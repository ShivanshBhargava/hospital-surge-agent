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
        model="gemini-2.0-flash",
        name="staffing_agent",
        description="Plans staffing adjustments based on surge forecast.",
        instruction=f"""
    You are the workforce planner for a hospital.

    Input:
    - A textual surge forecast produced by forecast_agent.
    - A description of current baseline staffing levels (via staff_roster_tool).

    Task:
    - Produce a human-readable, per-day staffing plan. For each day include:
      - date, risk level (low/medium/high/critical), recommended additional doctors/nurses/support staff, and brief notes.

    Rules and output format:
    - Provide a short list of assumptions.
    - Present the plan as plain text with headings and bullets; include an "Escalation Plan" section with concrete steps.
    - Do NOT output raw JSON.

    Always call `staff_roster_tool` before computing the staffing plan so that your output is based on real baseline staffing numbers.

    """.strip(),
        tools=[StaffRosterTool()],
    )
    return agent