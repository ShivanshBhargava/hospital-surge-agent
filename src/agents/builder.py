# src/agents/builder.py
from ..llm_setup import configure_genai
from .orchestrator import build_orchestrator_agent

def get_hospital_orchestrator():
    """
    Convenience function to configure the LLM client and build the orchestrator.
    """
    configure_genai()
    return build_orchestrator_agent()
