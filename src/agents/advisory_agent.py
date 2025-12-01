# src/agents/advisory_agent.py
from google.adk.agents import LlmAgent

ADVISORY_SCHEMA_DESCRIPTION = """
You output a JSON dictionary with:
- "overall_risk_summary": short paragraph in simple language.
- "patient_advisories": list of objects with:
    - "channel": one of ["sms", "email", "website_banner", "social_media"].
    - "target_group": e.g. "elderly", "asthma", "general public".
    - "message": the exact text to send or display (<= 280 characters when possible).
    - "priority": one of ["low", "medium", "high"].
- "internal_notes": short text for hospital leadership only.
"""

def build_advisory_agent() -> LlmAgent:
    """
    Agent that turns surge forecast into patient advisory messaging.
    """
    agent = LlmAgent(
        model="gemini-2.0-flash",
        name="advisory_agent",
        description="Creates patient-facing advisories based on surge risk.",
                instruction=f"""
You are the communications officer for the hospital.

Input:
- A textual surge forecast from forecast_agent.
- Optionally: specific risk factors like pollution spikes or festival crowds.

Task:
- Create clear, calm, and practical advisories for patients and the public.
    - Indicate when to avoid crowds, when to use teleconsultation, when to wear masks, and which groups should be extra careful.

Tone and output format:
- Use a reassuring, honest tone. Avoid panic.
- Produce human-readable advisories formatted as plain text. Provide channel-specific short messages (sms/email/website/social) and short internal notes for leadership.
- Do NOT output raw JSON.

""".strip(),
    )
    return agent
