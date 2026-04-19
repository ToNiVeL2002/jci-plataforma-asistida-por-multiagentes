"""
Agente de seguimiento de tareas.
Detecta tareas por vencer y envía correos de recordatorio automaticamente.
"""

from google.adk.agents import Agent
from .tools import tool_obtener_tareas, tool_enviar_correo


GEMINI_MODEL = "gemini-2.5-flash"


root_agent = Agent(
    name="agente_seguimiento",
    model=GEMINI_MODEL,
    description="Agente que revisa tareas próximas a vencer y envía recordatorios por correo.",
    instruction="""
Eres un agente automatizado de seguimiento para la plataforma JCI Emprendedores.

Tu único objetivo es ejecutar el siguiente proceso de forma completa y ordenada:

**PROCESO A EJECUTAR:**

1. Llama a `obtener_tareas_proximas_a_vencer` para obtener todas las tareas pendientes
   que vencen en 2 días o menos.

2. Si no hay tareas (`cantidad == 0`), reporta que no hay recordatorios que enviar y termina.

3. Si hay tareas, por cada una de ellas:
   - Llama a `enviar_correo_recordatorio` con los datos de esa tarea y del emprendedor.
   - Registra si el correo fue enviado exitosamente o si hubo un error.

4. Al finalizar, genera un resumen indicando:
   - Cuántos correos se intentaron enviar.
   - Cuántos fueron exitosos.
   - Si hubo algún error, menciona cuál fue.

**REGLAS IMPORTANTES:**
- No omitas ninguna tarea. Envía el correo a cada emprendedor de la lista.
- Si el email de un emprendedor está vacío, omite esa tarea e indícalo en el resumen.
- Ejecuta todo siempre, no pidas confirmación al usuario.
""",
    tools=[tool_obtener_tareas, tool_enviar_correo],
)
