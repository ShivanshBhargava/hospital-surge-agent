# src/tools/hospital_data_adk_tool.py
from google.adk.tools import FunctionTool
from typing import List, Dict
from .hospital_data_tools import read_recent_admissions

class HospitalAdmissionsTool(FunctionTool):
    """
    ADK wrapper to expose the admissions reader to agents.
    """
    name = "hospital_admissions_tool"
    description = "Reads recent hospital patient admissions (last N days)."

    def __call__(self, days: int = 14) -> List[Dict]:
        return read_recent_admissions(days)
