# src/agents/staffing_agent.py
from google.adk.agents import LlmAgent
from src.tools.roster_tool import StaffRosterTool

STAFFING_SCHEMA_DESCRIPTION = """
You output a JSON dictionary with:
- "assumptions": list of strings summarizing key assumptions.
- "per_day_plan": list of objects with:
    - "date": ISO date string.
    - "risk_level": one of ["low", "medium", "high", "critical"].
    - "recommended_additional_doctors": integer.
    - "recommended_additional_nurses": integer.
    - "recommended_support_staff": integer.
    - "notes": short explanation.
- "escalation_plan": short free-text string describing backup plans
  (on-call staff, partner hospitals, elective surgery postponement, etc.).
"""

def build_staffing_agent() -> LlmAgent:
    """
    Agent that turns a surge forecast + current staffing snapshot
    into a concrete staffing plan.
    """
    agent = LlmAgent(
        model="gemini-2.5-flash",
        name="staffing_agent",
        description="Plans staffing adjustments based on surge forecast.",
        instruction=f"""
You are the workforce planner for a hospital.

Input:
- A JSON surge forecast produced by the forecast_agent.
- A description of current baseline staffing levels.

Task:
- Produce a risk-aware staffing plan for each forecast day.

Rules:
- Increase staff on high/critical days.
- Prefer reallocating / shifting before hiring.
- Highlight when elective procedures should be reduced.

ALWAYS respond in valid JSON following this schema:

{STAFFING_SCHEMA_DESCRIPTION}

Always call staff_roster_tool before computing the staffing plan so that
your output is based on real baseline staffing numbers.

""".strip(),
        tools=[StaffRosterTool],
    )
    return agent