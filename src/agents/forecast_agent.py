# src/agents/forecast_agent.py
from google.adk.agents import LlmAgent
from src.tools.hospital_data_adk_tool import HospitalAdmissionsTool
from src.tools.pollution_api_tool import PollutionForecastTool

FORECAST_SCHEMA_DESCRIPTION = """
You output a JSON dictionary with:
- "horizon_days": integer, how many days ahead you are forecasting.
- "daily_forecast": list of objects, each with:
    - "date": ISO date string, e.g. "2025-11-15".
    - "surge_risk": one of ["low", "medium", "high", "critical"].
    - "expected_admissions": approximate integer count for total patients.
    - "main_drivers": list of strings, e.g. ["festival", "pollution", "flu-season"].
- "notes": short free-text reasoning.
"""

def build_forecast_agent() -> LlmAgent:
    """
    Build an LLM agent responsible for forecasting patient surges.

    Later we will attach tools:
      - hospital historical admissions tool
      - pollution / weather / festival tools
    For now it only uses its own reasoning.
    """
    agent = LlmAgent(
        model="gemini-2.0-flash",
        name="forecast_agent",
        description="Forecasts hospital patient surges based on events like festivals, pollution spikes, or epidemics.",
        instruction=f"""
      You are an operations analytics assistant for a large urban hospital.

      Your job is to forecast patient surges in the next N days given:
      - recent admissions and bed occupancy (via tools)
      - time of year, festivals, pollution levels, epidemic hints
      - the hospital is in a large Indian metro with strong festival effects

      Guidance for output:
      - Produce a clear human-readable plain-text forecast with a short heading, a 1-2 sentence summary, and a per-day bullet list for the horizon.
      - Under each date, include: risk level (low/medium/high/critical), expected admissions (approx.), and main drivers.
      - Explicitly list assumptions at the end of the forecast.
      - Do NOT output raw JSON. Use headings and bullets for readability.

      When you need recent admissions data, call tool `hospital_admissions_tool` (e.g. `{"days":14}`) before predicting surges.
      When location coordinates are provided, call `pollution_forecast_tool` to incorporate PM2.5/AQI.
      If a tool fails, continue with a best-effort textual forecast and note the missing data.

      """.strip(),
        tools=[HospitalAdmissionsTool(),
        PollutionForecastTool()]
    )
    return agent
