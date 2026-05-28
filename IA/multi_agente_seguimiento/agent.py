"""
Punto de entrada ADK — expone root_agent para `adk web` / `adk api_server`.
"""

from .agents import root_agent

__all__ = ["root_agent"]
