# src/tools/hospital_data_adk_tool.py
from __future__ import annotations
from google.adk.tools import FunctionTool
from typing import Any
from .hospital_data_tools import read_recent_admissions

def hospital_admissions_func(days: int = 14) -> list[dict[str, Any]]:
    """Reads recent hospital patient admissions (last N days)."""
    return read_recent_admissions(days)

class HospitalAdmissionsTool(FunctionTool):
    """
    ADK wrapper to expose the admissions reader to agents.
    """
    def __init__(self):
        super().__init__(func=hospital_admissions_func)
