"""
Configuración para el diagnóstico de emprendedores.
Las preguntas se obtienen de la base de datos mediante la API del backend.
Este módulo contiene los mapeos de áreas y reglas de consistencia.

Áreas:
  cf  — Costos y Finanzas
  gp  — Gestión y Planificación
  m   — Marketing
  v   — Ventas
  tp  — Tecnología y Procesos
  rh  — Recursos Humanos
  ec  — Economía del Cuidado
"""

# ──────────────────────────────────────────────────────────
# Mapeo de id_area (DB) → código de área interno
# ──────────────────────────────────────────────────────────
AREA_MAP = {
    1: "cf",
    2: "gp",
    3: "m",
    4: "v",
    5: "tp",
    6: "rh",
    7: "ec",
}

AREA_NAMES = {
    "cf": "Costos y Finanzas",
    "gp": "Gestión y Planificación",
    "m":  "Marketing",
    "v":  "Ventas",
    "tp": "Tecnología y Procesos",
    "rh": "Recursos Humanos",
    "ec": "Economía del Cuidado",
}


# ──────────────────────────────────────────────────────────
# Mapeo de id_pregunta (DB) → key para reglas de consistencia
# ──────────────────────────────────────────────────────────
# Este mapeo es NECESARIO para que las reglas de consistencia
# puedan identificar qué preguntas comparar entre sí.
# Si se agrega una nueva pregunta a la DB y no necesita
# verificación de consistencia, no es necesario agregarla aquí.
# Las preguntas sin key en este mapeo funcionan normalmente,
# solo no participan en las verificaciones de consistencia.
# ──────────────────────────────────────────────────────────
QUESTION_KEY_MAP = {
    1:  "registro_ingresos",
    2:  "punto_equilibrio",
    3:  "metas_actividades",
    4:  "revision_avances",
    5:  "estrategia_promocion",
    6:  "cliente_ideal",
    7:  "meta_ventas",
    8:  "seguimiento_clientes",
    9:  "herramientas_digitales",
    10: "procesos_documentados",
    11: "roles_responsabilidades",
    12: "capacitacion_equipo",
    13: "horas_cuidado",
    14: "oportunidades_perdidas",
}


# ──────────────────────────────────────────────────────────
# Reglas de consistencia entre respuestas
# ──────────────────────────────────────────────────────────
# Cada regla define pares de preguntas cuyas respuestas
# deben ser coherentes entre sí. El LLM evaluará si existe
# inconsistencia usando la descripción como guía.
# ──────────────────────────────────────────────────────────

CONSISTENCY_RULES = [
    {
        # Regla 1: punto de equilibrio vs meta de ventas
        "keys": ["punto_equilibrio", "meta_ventas"],
        "description": (
            "Si el emprendedor menciona cuánto debe vender para cubrir gastos "
            "(punto de equilibrio) y su meta de ventas es menor a esa cantidad, "
            "existe una inconsistencia financiera grave."
        ),
        "areas_affected": ["cf", "v"],
        "penalty": 15,
    },
    {
        # Regla 2: metas sin revisión
        "keys": ["metas_actividades", "revision_avances"],
        "description": (
            "Si el emprendedor dice tener metas definidas pero no revisa "
            "sus avances regularmente, la planificación no es efectiva."
        ),
        "areas_affected": ["gp"],
        "penalty": 10,
    },
    {
        # Regla 3: estrategia de promoción sin conocer al cliente
        "keys": ["estrategia_promocion", "cliente_ideal"],
        "description": (
            "Si el emprendedor dice tener una estrategia de promoción pero "
            "no conoce a su cliente ideal, la estrategia carece de enfoque."
        ),
        "areas_affected": ["m"],
        "penalty": 10,
    },
    {
        # Regla 4: procesos documentados sin herramientas digitales
        "keys": ["procesos_documentados", "herramientas_digitales"],
        "description": (
            "Si el emprendedor dice tener procesos documentados pero no usa "
            "herramientas digitales, la documentación puede no ser accesible ni escalable."
        ),
        "areas_affected": ["tp"],
        "penalty": 10,
    },
    {
        # Regla 5: seguimiento de clientes sin metas de ventas
        "keys": ["seguimiento_clientes", "meta_ventas"],
        "description": (
            "Si el emprendedor hace seguimiento a clientes pero no tiene "
            "metas de ventas definidas, el seguimiento carece de dirección."
        ),
        "areas_affected": ["v"],
        "penalty": 10,
    },
]
