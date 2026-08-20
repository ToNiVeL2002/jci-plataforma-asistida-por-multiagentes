"""
Tools del agente de seguimiento.
Consume APIs del backend para obtener tareas y datos de usuarios.
Envía correos de recordatorio por SMTP.
"""

import os
import smtplib
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Any

from google.adk.tools import FunctionTool


BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
EMAIL_SENDER = os.environ.get("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")


# ---------------------------------------------------------------------------
# Tool 1: Obtener tareas próximas a vencer desde el backend
# ---------------------------------------------------------------------------

def obtener_tareas_proximas_a_vencer() -> dict[str, Any]:
    """
    Consulta el backend para obtener todas las tareas pendientes que vencen
    en 2 días o menos a partir de ahora.

    Returns:
        Un diccionario con la lista de tareas y la cantidad total.
        Cada tarea incluye: id_tarea, titulo, descripcion, fecha_expiracion,
        estado, nombre del emprendedor y su email.
    """
    try:
        response = requests.get(
            f"{BACKEND_URL}/seguimiento/tareas-proximas",
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        return {"error": str(e), "cantidad": 0, "tareas": []}


# ---------------------------------------------------------------------------
# Tool 2: Enviar correo de recordatorio
# ---------------------------------------------------------------------------

def enviar_correo_recordatorio(
    email_destinatario: str,
    nombre_emprendedor: str,
    titulo_tarea: str,
    descripcion_tarea: str,
    fecha_expiracion: str,
) -> dict[str, Any]:
    """
    Envía un correo electrónico de recordatorio al emprendedor sobre una tarea próxima a vencer.

    Args:
        email_destinatario: Correo del emprendedor.
        nombre_emprendedor: Nombre completo del emprendedor.
        titulo_tarea: Título de la tarea.
        descripcion_tarea: Descripción de la tarea.
        fecha_expiracion: Fecha límite de la tarea (ISO 8601).

    Returns:
        dict indicando éxito o error.
    """
    try:
        # Formatear fecha amigable
        try:
            fecha_dt = datetime.fromisoformat(fecha_expiracion.replace("Z", "+00:00"))
            fecha_legible = fecha_dt.strftime("%d/%m/%Y a las %H:%M")
        except Exception:
            fecha_legible = fecha_expiracion

        asunto = f"⏰ Recordatorio: Tu tarea \"{titulo_tarea}\" vence pronto"

        cuerpo_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
          <div style="max-width: 600px; margin: auto; background: white; border-radius: 10px;
                      padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h2 style="color: #2563eb;">⏰ Recordatorio de tarea pendiente</h2>
            <p>Hola <strong>{nombre_emprendedor}</strong>,</p>
            <p>Te recordamos que tienes una tarea pendiente que vence en menos de 2 días:</p>
            <div style="background: #eff6ff; border-left: 4px solid #2563eb;
                        padding: 15px; border-radius: 5px; margin: 20px 0;">
              <h3 style="margin: 0 0 8px 0; color: #1d4ed8;">{titulo_tarea}</h3>
              <p style="margin: 0; color: #374151;">{descripcion_tarea or "Sin descripción adicional."}</p>
              <p style="margin: 10px 0 0 0; color: #ef4444; font-weight: bold;">
                📅 Fecha límite: {fecha_legible}
              </p>
            </div>
            <p>Por favor, ingresa a la plataforma JCI para completar tu tarea.</p>
            <p style="color: #6b7280; font-size: 13px; margin-top: 30px;">
              Este es un correo automático. Por favor no respondas a este mensaje.
            </p>
          </div>
        </body>
        </html>
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = asunto
        msg["From"] = EMAIL_SENDER
        msg["To"] = email_destinatario
        msg.attach(MIMEText(cuerpo_html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, email_destinatario, msg.as_string())

        return {
            "exito": True,
            "mensaje": f"Correo enviado a {email_destinatario} correctamente.",
        }

    except smtplib.SMTPAuthenticationError:
        return {"exito": False, "error": "Error de autenticación SMTP. Verifica EMAIL_SENDER y EMAIL_PASSWORD."}
    except Exception as e:
        return {"exito": False, "error": str(e)}


# ---------------------------------------------------------------------------
# Registro de tools para el agente
# ---------------------------------------------------------------------------

tool_obtener_tareas = FunctionTool(func=obtener_tareas_proximas_a_vencer)
tool_enviar_correo = FunctionTool(func=enviar_correo_recordatorio)
