"""
ADK Tools — funciones que el OrchestratorAgent invoca para gestionar el diagnóstico.
Todas las funciones usan tool_context.state para mantener el estado de la sesión.
"""

import os
import requests
from google.adk.tools import ToolContext
from .questions import AREA_MAP, QUESTION_KEY_MAP, AREA_NAMES, CONSISTENCY_RULES


BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")


# ──────────────────────────────────────────────
# Rubros válidos para el emprendimiento
# ──────────────────────────────────────────────
RUBROS_VALIDOS = [
    "Comercio y ventas",
    "Gastronomía",
    "Servicios personales",
    "Artes y manualidades",
    "Tecnología y educación",
    "Agro y producción",
    "Otros",
]


# ──────────────────────────────────────────────
# Helpers internos
# ──────────────────────────────────────────────

def _init_state_if_needed(state: dict) -> None:
    """Inicializa el estado del diagnóstico si aún no existe."""
    if "current_question_id" not in state:
        state["current_question_id"] = 1  # Las preguntas en la DB empiezan en 1
    if "current_question" not in state:
        state["current_question"] = None  # Datos de la pregunta actual (del API)
    if "diagnostic_finished" not in state:
        state["diagnostic_finished"] = False
    if "questions_answered" not in state:
        state["questions_answered"] = 0
    if "scores" not in state:
        state["scores"] = {
            "cf": [], "gp": [], "m": [],
            "v": [],  "tp": [], "rh": [],
            "ec": []
        }
    if "answers" not in state:
        state["answers"] = []
    if "results" not in state:
        state["results"] = None
    # ── Estado para evaluación contextual ──
    if "respuestas" not in state:
        # Dict indexado por key de pregunta, para acceso rápido
        state["respuestas"] = {}
    if "inconsistencias" not in state:
        # Lista de inconsistencias detectadas entre respuestas
        state["inconsistencias"] = []
    # ── Estado para contexto del emprendimiento ──
    if "contexto_emprendimiento" not in state:
        state["contexto_emprendimiento"] = {
            "nombre_emprendedor": "",
            "nombre_emprendimiento": "",
            "rubro": "",
            "anos_funcionamiento": 0,
            "numero_personal": 0,
            "ventas_mensuales_promedio": 0,
        }


# ──────────────────────────────────────────────
# Tool: registrar contexto del emprendimiento
# ──────────────────────────────────────────────

def register_context(
    nombre_emprendedor: str,
    nombre_emprendimiento: str,
    rubro: str,
    anos_funcionamiento: int,
    numero_personal: int,
    ventas_mensuales_promedio: int,
    tool_context: ToolContext,
) -> dict:
    """Registra el contexto del emprendimiento antes de iniciar el diagnóstico.

    Esta información se usa para personalizar preguntas, ajustar
    la evaluación según el rubro y detectar inconsistencias financieras.

    Args:
        nombre_emprendedor: Nombre del emprendedor.
        nombre_emprendimiento: Nombre del negocio o emprendimiento.
        rubro: Rubro del negocio (ej: Gastronomía, Tecnología y educación).
        anos_funcionamiento: Años que lleva funcionando el emprendimiento.
        numero_personal: Número de personas que trabajan en el emprendimiento.
        ventas_mensuales_promedio: Ventas mensuales promedio en bolivianos.

    Returns:
        dict: Confirmación del registro con el contexto guardado.
    """
    _init_state_if_needed(tool_context.state)

    contexto = {
        "nombre_emprendedor": nombre_emprendedor,
        "nombre_emprendimiento": nombre_emprendimiento,
        "rubro": rubro,
        "anos_funcionamiento": anos_funcionamiento,
        "numero_personal": numero_personal,
        "ventas_mensuales_promedio": ventas_mensuales_promedio,
    }
    tool_context.state["contexto_emprendimiento"] = contexto

    # Determinar si es un negocio maduro (>2 años)
    es_maduro = anos_funcionamiento > 2

    return {
        "status": "success",
        "message": f"Contexto registrado para {nombre_emprendimiento} ({rubro}).",
        "contexto": contexto,
        "es_negocio_maduro": es_maduro,
        "rubros_validos": RUBROS_VALIDOS,
    }


# ──────────────────────────────────────────────
# Tool: obtener siguiente pregunta
# ──────────────────────────────────────────────

def get_next_question(tool_context: ToolContext) -> dict:
    """Obtiene la siguiente pregunta del diagnóstico desde el backend (base de datos).

    Llama a GET /preguntas/{id} del backend. Si la pregunta existe,
    la guarda en el estado y la devuelve. Si recibe 404, el diagnóstico
    ha finalizado.

    Returns:
        dict: Con claves 'status', 'question' (o 'message' si finalizó),
              'question_number' y 'total_questions'.
    """
    _init_state_if_needed(tool_context.state)

    if tool_context.state.get("diagnostic_finished", False):
        return {
            "status": "finished",
            "message": "Todas las preguntas han sido respondidas. Llama a compute_results para calcular los resultados finales."
        }

    question_id = tool_context.state["current_question_id"]

    try:
        response = requests.get(f"{BACKEND_URL}/preguntas/{question_id}")

        if response.status_code == 200:
            data = response.json()
            # Mapear id_area numérico a código de área
            area_code = AREA_MAP.get(data["id_area"], "cf")
            # Mapear id_pregunta a key para reglas de consistencia
            key = QUESTION_KEY_MAP.get(data["id_pregunta"], f"pregunta_{data['id_pregunta']}")

            # Guardar la pregunta actual en el estado
            current_question = {
                "id": data["id_pregunta"],
                "area": area_code,
                "key": key,
                "text": data["enunciado"],
            }
            tool_context.state["current_question"] = current_question

            return {
                "status": "success",
                "question_number": tool_context.state["questions_answered"] + 1,
                "question_id": data["id_pregunta"],
                "area": area_code,
                "area_name": AREA_NAMES.get(area_code, area_code),
                "text": data["enunciado"],
                "key": key,
            }

        elif response.status_code == 404:
            # No hay más preguntas
            tool_context.state["diagnostic_finished"] = True
            tool_context.state["current_question"] = None
            return {
                "status": "finished",
                "message": "Todas las preguntas han sido respondidas. Llama a compute_results para calcular los resultados finales."
            }

        else:
            return {
                "status": "error",
                "message": f"Error HTTP {response.status_code}: {response.text}"
            }

    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "message": "No se pudo conectar con el backend. Verifica que esté ejecutándose en " + BACKEND_URL
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error al obtener la pregunta: {str(e)}"
        }


# ──────────────────────────────────────────────
# Tool: registrar respuesta del usuario
# ──────────────────────────────────────────────

def register_answer(answer: str, tool_context: ToolContext) -> dict:
    """Registra la respuesta textual del usuario para la pregunta actual.

    Guarda la respuesta en la lista de answers Y también en el dict
    respuestas indexado por key para consultas contextuales.

    Args:
        answer: La respuesta del usuario a la pregunta actual.

    Returns:
        dict: Confirmación con el índice de la pregunta registrada.
    """
    _init_state_if_needed(tool_context.state)
    question = tool_context.state.get("current_question")

    if not question:
        return {"status": "error", "message": "No hay pregunta activa para registrar respuesta."}

    question_id = tool_context.state["current_question_id"]

    # Guardar en lista de answers
    tool_context.state["answers"] = tool_context.state.get("answers", []) + [{
        "question_id": question["id"],
        "area": question["area"],
        "key": question["key"],
        "text": question["text"],
        "user_answer": answer,
    }]

    # Guardar respuesta indexada por key para consultas rápidas (consistencia)
    respuestas = tool_context.state.get("respuestas", {})
    respuestas[question["key"]] = {
        "question_id": question["id"],
        "area": question["area"],
        "text": question["text"],
        "answer": answer,
    }
    tool_context.state["respuestas"] = respuestas

    return {
        "status": "success",
        "message": f"Respuesta registrada para pregunta {question_id}.",
        "area": question["area"],
        "key": question["key"],
    }


# ──────────────────────────────────────────────
# Tool: registrar puntaje
# ──────────────────────────────────────────────

def register_score(score: int, reason: str, tool_context: ToolContext) -> dict:
    """Registra el puntaje (0-100) para la pregunta actual y avanza a la siguiente.

    Args:
        score: Puntaje numérico de 0 a 100.
        reason: Breve justificación del puntaje asignado.

    Returns:
        dict: Confirmación y si hay más preguntas o el diagnóstico terminó.
    """
    _init_state_if_needed(tool_context.state)
    question = tool_context.state.get("current_question")

    if not question:
        return {"status": "error", "message": "No hay pregunta activa para registrar puntaje."}

    area = question["area"]

    # Append score al área correspondiente
    current_scores = tool_context.state.get("scores", {})
    area_scores = current_scores.get(area, [])
    area_scores = area_scores + [score]
    current_scores[area] = area_scores
    tool_context.state["scores"] = current_scores

    # Avanzar al siguiente ID de pregunta
    current_id = tool_context.state["current_question_id"]
    tool_context.state["current_question_id"] = current_id + 1
    tool_context.state["current_question"] = None  # Limpiar pregunta actual
    tool_context.state["questions_answered"] = tool_context.state.get("questions_answered", 0) + 1

    return {
        "status": "success",
        "message": f"Puntaje {score} registrado en área '{AREA_NAMES[area]}'. Razón: {reason}",
        "questions_answered": tool_context.state["questions_answered"],
    }


# ──────────────────────────────────────────────
# Tool: verificar inconsistencias contextuales
# ──────────────────────────────────────────────

def check_inconsistencies(tool_context: ToolContext) -> dict:
    """Verifica si existen inconsistencias entre respuestas ya registradas.

    Compara pares de respuestas según las reglas de consistencia definidas.
    Si ambas respuestas de un par existen, las incluye en el resultado
    para que el ScoreAgent/Orchestrator evalúe si hay inconsistencia.

    Debe llamarse después de registrar cada respuesta.

    Returns:
        dict: Lista de pares de respuestas que deben ser evaluados por
              consistencia, junto con la descripción de la regla.
    """
    _init_state_if_needed(tool_context.state)
    respuestas = tool_context.state.get("respuestas", {})
    inconsistencias_previas = tool_context.state.get("inconsistencias", [])

    # Obtener keys de inconsistencias ya detectadas para no repetir
    reglas_ya_evaluadas = {inc.get("rule_keys", "") for inc in inconsistencias_previas}

    pairs_to_evaluate = []

    for rule in CONSISTENCY_RULES:
        keys = rule["keys"]
        rule_id = "+".join(sorted(keys))

        # Solo evaluar si ambas respuestas existen y no se evaluó antes
        if rule_id not in reglas_ya_evaluadas and all(k in respuestas for k in keys):
            pair_data = {
                "rule_id": rule_id,
                "rule_description": rule["description"],
                "areas_affected": rule["areas_affected"],
                "penalty": rule["penalty"],
                "responses": {
                    k: {
                        "question": respuestas[k]["text"],
                        "answer": respuestas[k]["answer"],
                    }
                    for k in keys
                },
            }
            pairs_to_evaluate.append(pair_data)

    # ── Verificar inconsistencia ventas_promedio vs punto_equilibrio del contexto ──
    contexto = tool_context.state.get("contexto_emprendimiento", {})
    ventas_promedio = contexto.get("ventas_mensuales_promedio", 0)
    if (
        "contexto_vs_punto_equilibrio" not in reglas_ya_evaluadas
        and ventas_promedio > 0
        and "punto_equilibrio" in respuestas
    ):
        pairs_to_evaluate.append({
            "rule_id": "contexto_vs_punto_equilibrio",
            "rule_description": (
                f"Las ventas mensuales promedio reportadas ({ventas_promedio}) "
                "deben compararse con el punto de equilibrio mencionado. "
                "Si las ventas promedio son menores al punto de equilibrio, "
                "el negocio está operando a pérdida."
            ),
            "areas_affected": ["cf"],
            "penalty": 15,
            "responses": {
                "ventas_promedio_contexto": {
                    "question": "Ventas mensuales promedio (dato del contexto)",
                    "answer": str(ventas_promedio),
                },
                "punto_equilibrio": {
                    "question": respuestas["punto_equilibrio"]["text"],
                    "answer": respuestas["punto_equilibrio"]["answer"],
                },
            },
        })

    if not pairs_to_evaluate:
        return {
            "status": "no_pairs",
            "message": "No hay pares de respuestas nuevos para evaluar consistencia.",
        }

    return {
        "status": "pairs_found",
        "message": f"Se encontraron {len(pairs_to_evaluate)} par(es) de respuestas para evaluar consistencia.",
        "pairs": pairs_to_evaluate,
    }


# ──────────────────────────────────────────────
# Tool: registrar inconsistencia detectada
# ──────────────────────────────────────────────

def register_inconsistency(
    rule_keys: str,
    description: str,
    penalty: int,
    areas_affected: list[str],
    tool_context: ToolContext,
) -> dict:
    """Registra una inconsistencia detectada entre respuestas.

    Guarda la inconsistencia en el estado y aplica la penalización
    a los scores de las áreas afectadas.

    Args:
        rule_keys: Identificador de la regla (ej: "meta_ventas+punto_equilibrio").
        description: Descripción de la inconsistencia encontrada.
        penalty: Puntos de penalización a aplicar.
        areas_affected: Lista de códigos de área afectadas (ej: ["cf", "v"]).

    Returns:
        dict: Confirmación del registro.
    """
    _init_state_if_needed(tool_context.state)

    # Registrar la inconsistencia
    inconsistencias = tool_context.state.get("inconsistencias", [])
    inconsistencias = inconsistencias + [{
        "rule_keys": rule_keys,
        "description": description,
        "penalty": penalty,
        "areas_affected": areas_affected,
    }]
    tool_context.state["inconsistencias"] = inconsistencias

    return {
        "status": "success",
        "message": f"Inconsistencia registrada: {description}. Penalización de {penalty} pts en áreas: {', '.join(areas_affected)}.",
        "total_inconsistencies": len(inconsistencias),
    }


# ──────────────────────────────────────────────
# Tool: calcular resultados finales
# ──────────────────────────────────────────────

def compute_results(tool_context: ToolContext) -> dict:
    """Calcula los promedios por área y el puntaje general del diagnóstico.

    Aplica penalizaciones por inconsistencias detectadas y por madurez
    del negocio (negocios con >2 años sin procesos básicos reciben penalty).
    Debe llamarse cuando todas las preguntas han sido respondidas.

    Returns:
        dict: Promedios por área, puntaje final, nivel de madurez e inconsistencias.
    """
    _init_state_if_needed(tool_context.state)
    scores = tool_context.state.get("scores", {})
    inconsistencias = tool_context.state.get("inconsistencias", [])
    contexto = tool_context.state.get("contexto_emprendimiento", {})

    # ── Penalización por madurez del negocio ──
    # Si el negocio tiene >2 años, se esperan procesos más formales.
    # Si carece de ellos, se aplica una penalización adicional.
    anos = contexto.get("anos_funcionamiento", 0)
    maturity_penalties = {}
    maturity_warnings = []
    if anos > 2:
        respuestas = tool_context.state.get("respuestas", {})
        # Verificar si tiene registro financiero
        resp_registro = respuestas.get("registro_ingresos", {})
        if resp_registro:
            # Si la respuesta sugiere que no lleva registro, penalizar
            ans_lower = resp_registro.get("answer", "").lower()
            if any(neg in ans_lower for neg in ["no", "nunca", "nada", "no llevo"]):
                maturity_penalties["cf"] = maturity_penalties.get("cf", 0) + 5
                maturity_warnings.append(
                    f"Negocio con {anos} años sin registro de ingresos/egresos."
                )
        # Verificar si tiene metas de ventas
        resp_metas = respuestas.get("meta_ventas", {})
        if resp_metas:
            ans_lower = resp_metas.get("answer", "").lower()
            if any(neg in ans_lower for neg in ["no", "nunca", "nada", "no tengo"]):
                maturity_penalties["v"] = maturity_penalties.get("v", 0) + 5
                maturity_warnings.append(
                    f"Negocio con {anos} años sin metas de ventas claras."
                )
        # Verificar procesos documentados
        resp_procesos = respuestas.get("procesos_documentados", {})
        if resp_procesos:
            ans_lower = resp_procesos.get("answer", "").lower()
            if any(neg in ans_lower for neg in ["no", "nunca", "nada"]):
                maturity_penalties["tp"] = maturity_penalties.get("tp", 0) + 5
                maturity_warnings.append(
                    f"Negocio con {anos} años sin procesos documentados."
                )

    # ── Calcular penalizaciones acumuladas por área (inconsistencias + madurez) ──
    penalties_by_area = {}
    for inc in inconsistencias:
        for area in inc.get("areas_affected", []):
            penalties_by_area[area] = penalties_by_area.get(area, 0) + inc.get("penalty", 0)
    # Sumar penalizaciones por madurez
    for area, pen in maturity_penalties.items():
        penalties_by_area[area] = penalties_by_area.get(area, 0) + pen

    area_averages = {}
    total_sum = 0
    total_count = 0

    for area_code, area_name in AREA_NAMES.items():
        area_scores = scores.get(area_code, [])
        if area_scores:
            raw_avg = round(sum(area_scores) / len(area_scores), 1)
            penalty = penalties_by_area.get(area_code, 0)
            adjusted_avg = max(0, round(raw_avg - penalty, 1))
            area_averages[area_code] = {
                "name": area_name,
                "raw_average": raw_avg,
                "penalty_applied": penalty,
                "adjusted_average": adjusted_avg,
                "scores": area_scores,
            }
            total_sum += adjusted_avg * len(area_scores)
            total_count += len(area_scores)
        else:
            area_averages[area_code] = {
                "name": area_name,
                "raw_average": 0,
                "penalty_applied": 0,
                "adjusted_average": 0,
                "scores": [],
            }

    final_score = round(total_sum / total_count, 1) if total_count > 0 else 0

    # Determinar nivel de madurez del emprendimiento
    if final_score >= 80:
        maturity = "Avanzado"
    elif final_score >= 60:
        maturity = "Intermedio"
    elif final_score >= 40:
        maturity = "Básico"
    else:
        maturity = "Inicial"

    results = {
        "area_averages": area_averages,
        "final_score": final_score,
        "maturity_level": maturity,
        "total_questions_answered": total_count,
        "inconsistencies_found": len(inconsistencias),
        "inconsistencies": [
            {"description": inc["description"], "areas": inc["areas_affected"], "penalty": inc["penalty"]}
            for inc in inconsistencias
        ],
        # ── Contexto del emprendimiento incluido en resultados ──
        "contexto_emprendimiento": contexto,
        "maturity_warnings": maturity_warnings,
    }

    tool_context.state["results"] = results

    return {
        "status": "success",
        "results": results,
    }


# ──────────────────────────────────────────────
# Tool: crear diagnóstico en la base de datos
# ──────────────────────────────────────────────

def create_diagnostico(tool_context: ToolContext) -> dict:
    """Crea un nuevo registro de diagnóstico en la base de datos.

    Debe llamarse al INICIO del diagnóstico, antes de la primera pregunta.
    Guarda el id_diagnostico en el estado para uso posterior.

    Returns:
        dict: Confirmación con el id_diagnostico creado.
    """
    _init_state_if_needed(tool_context.state)

    id_usuario = tool_context.state.get("id_usuario")
    if not id_usuario:
        return {
            "status": "error",
            "message": "No se encontró id_usuario en el contexto.",
        }

    try:
        response = requests.post(
            f"{BACKEND_URL}/diagnostico",
            json={"id_usuario": id_usuario},
        )

        if response.status_code == 201:
            data = response.json()
            tool_context.state["id_diagnostico"] = data["id_diagnostico"]
            return {
                "status": "success",
                "id_diagnostico": data["id_diagnostico"],
                "message": "Diagnóstico creado exitosamente.",
            }
        else:
            return {
                "status": "error",
                "message": f"Error HTTP {response.status_code}: {response.text}",
            }

    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "message": "No se pudo conectar con el backend para crear el diagnóstico.",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error al crear diagnóstico: {str(e)}",
        }


# ──────────────────────────────────────────────
# Tool: guardar respuesta individual en la BD
# ──────────────────────────────────────────────

def save_answer_to_db(respuesta_usuario: str, puntaje: int, tool_context: ToolContext) -> dict:
    """Guarda una respuesta individual del usuario en la base de datos.

    Debe llamarse DESPUÉS de register_answer y register_score para cada pregunta.
    Usa id_diagnostico y current_question del estado.

    Args:
        respuesta_usuario: La respuesta textual del usuario.
        puntaje: El puntaje asignado a la respuesta (0-100).

    Returns:
        dict: Confirmación del guardado.
    """
    _init_state_if_needed(tool_context.state)

    id_diagnostico = tool_context.state.get("id_diagnostico")
    if not id_diagnostico:
        return {
            "status": "error",
            "message": "No se encontró id_diagnostico. ¿Se llamó a create_diagnostico?",
        }

    # Obtener los datos de la última respuesta registrada
    answers = tool_context.state.get("answers", [])
    if not answers:
        return {
            "status": "error",
            "message": "No hay respuestas registradas.",
        }

    last_answer = answers[-1]
    id_pregunta = last_answer["question_id"]

    try:
        response = requests.post(
            f"{BACKEND_URL}/diagnostico/detalle",
            json={
                "id_diagnostico": id_diagnostico,
                "id_pregunta": id_pregunta,
                "respuesta_usuario": respuesta_usuario,
                "puntaje": float(puntaje),
            },
        )

        if response.status_code == 201:
            data = response.json()
            return {
                "status": "success",
                "id_detalle": data["id_detalle"],
                "message": f"Respuesta guardada en la base de datos (pregunta {id_pregunta}).",
            }
        else:
            return {
                "status": "error",
                "message": f"Error HTTP {response.status_code}: {response.text}",
            }

    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "message": "No se pudo conectar con el backend para guardar la respuesta.",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error al guardar respuesta: {str(e)}",
        }


# ──────────────────────────────────────────────
# Tool: guardar resultados finales en la BD
# ──────────────────────────────────────────────

def save_results_to_db(conclusion: str, recomendaciones: str, tool_context: ToolContext) -> dict:
    """Guarda los resultados finales del diagnóstico en la base de datos.

    Debe llamarse AL FINAL del diagnóstico, después de compute_results,
    conclusion_tool y recommendation_tool.

    Args:
        conclusion: Texto de la conclusión generada por el ConclusionAgent.
        recomendaciones: Texto de las recomendaciones generadas por el RecommendationAgent.

    Returns:
        dict: Confirmación del guardado con el resultado final.
    """
    _init_state_if_needed(tool_context.state)

    id_diagnostico = tool_context.state.get("id_diagnostico")
    if not id_diagnostico:
        return {
            "status": "error",
            "message": "No se encontró id_diagnostico. ¿Se llamó a create_diagnostico?",
        }

    results = tool_context.state.get("results")
    if not results:
        return {
            "status": "error",
            "message": "No hay resultados calculados. ¿Se llamó a compute_results?",
        }

    # Extraer puntajes ajustados por área
    area_avgs = results.get("area_averages", {})
    puntaje_cf = round(area_avgs.get("cf", {}).get("adjusted_average", 0))
    puntaje_gp = round(area_avgs.get("gp", {}).get("adjusted_average", 0))
    puntaje_m = round(area_avgs.get("m", {}).get("adjusted_average", 0))
    puntaje_v = round(area_avgs.get("v", {}).get("adjusted_average", 0))
    puntaje_tp = round(area_avgs.get("tp", {}).get("adjusted_average", 0))
    puntaje_rh = round(area_avgs.get("rh", {}).get("adjusted_average", 0))
    puntaje_ec = round(area_avgs.get("ec", {}).get("adjusted_average", 0))

    puntaje_total = round(results.get("final_score", 0))

    # Determinar resultado
    if puntaje_total >= 66:
        resultado = "EXIMIDO"
    elif puntaje_total >= 30:
        resultado = "ACEPTADO"
    else:
        resultado = "RECHAZADO"

    # Formatear inconsistencias como texto
    inconsistencias_list = results.get("inconsistencies", [])
    inconsistencias_text = "No se detectaron inconsistencias en las respuestas del emprendedor."
    if inconsistencias_list:
        partes = []
        for inc in inconsistencias_list:
            areas_str = ", ".join(inc.get("areas", []))
            partes.append(
                f"- {inc['description']} (Áreas afectadas: {areas_str}, Penalización: {inc['penalty']} pts)"
            )
        inconsistencias_text = "\n".join(partes)

    try:
        response = requests.put(
            f"{BACKEND_URL}/diagnostico/{id_diagnostico}",
            json={
                "puntaje_total": puntaje_total,
                "conclusion": conclusion,
                "resultado": resultado,
                "puntaje_cf": puntaje_cf,
                "puntaje_gp": puntaje_gp,
                "puntaje_m": puntaje_m,
                "puntaje_v": puntaje_v,
                "puntaje_tp": puntaje_tp,
                "puntaje_rh": puntaje_rh,
                "puntaje_ec": puntaje_ec,
                "recomendaciones": recomendaciones,
                "inconsistencias": inconsistencias_text,
            },
        )

        if response.status_code == 200:
            return {
                "status": "success",
                "resultado": resultado,
                "puntaje_total": puntaje_total,
                "message": "Resultados guardados en la base de datos exitosamente.",
            }
        else:
            return {
                "status": "error",
                "message": f"Error HTTP {response.status_code}: {response.text}",
            }

    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "message": "No se pudo conectar con el backend para guardar resultados.",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error al guardar resultados: {str(e)}",
        }
