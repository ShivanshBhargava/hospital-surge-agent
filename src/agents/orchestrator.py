# src/agents/orchestrator.py
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool

from .forecast_agent import build_forecast_agent
from .staffing_agent import build_staffing_agent
from .supply_agent import build_supply_agent
from .advisory_agent import build_advisory_agent

from src.memory.session_store import SessionStore
from src.memory.memory_bank import MemoryBank

session = SessionStore()
memory_bank = MemoryBank()

def build_orchestrator_agent() -> LlmAgent:
    """
    Top-level orchestrator agent.

    It does not directly talk to tools (yet). Instead it delegates to
    specialist agents via AgentTool, making this a multi-agent system.
    """
    forecast_agent = build_forecast_agent()
    staffing_agent = build_staffing_agent()
    supply_agent = build_supply_agent()
    advisory_agent = build_advisory_agent()

    orchestrator = LlmAgent(
        model="gemini-2.5-pro",
        name="hospital_orchestrator",
        description=(
            "Coordinates forecasting, staffing, supply, and advisories "
            "for managing unpredictable hospital surges."
        ),
        instruction="""
You are the Chief Operations Orchestrator for a large urban hospital.

Your mission:
Given a request like "plan for the coming week" plus optional context
(e.g. festival schedule, pollution alerts, early epidemic signals),
you must:

1. Ask the forecast_agent (via tools) to produce a structured surge forecast.
2. Feed that forecast to staffing_agent to get a staffing plan.
3. Feed the same forecast to supply_agent to get a supply plan.
4. Feed the forecast (and optionally the staffing/supply outputs) to
   advisory_agent to generate patient advisories.
5. Synthesize everything into:
   - a natural language summary for leadership, and
   - a single JSON object containing:
       - "surge_forecast"
       - "staffing_plan"
       - "supply_plan"
       - "patient_advisories"

You should:
- Explicitly label assumptions.
- Be conservative about risk.
- Call the specialist agents instead of improvising details yourself.

If relevant past surge events exist in long-term memory, incorporate them.
Memory entries include:
- event_summary
- staffing_outcome
- supply_outcome
- success_indicators
- tags

Use them ONLY as guidance, not as deterministic rules.

Before calling any specialist agent, call MEMORY_RETRIEVAL (pseudo step).
I will provide you related memory snippets below when I run you.
Use them only to adjust your plan.


""".strip(),
        tools=[
            AgentTool(agent=forecast_agent),
            AgentTool(agent=staffing_agent),
            AgentTool(agent=supply_agent),
            AgentTool(agent=advisory_agent),
        ],
    )

    return orchestrator

def remember_outcome(forecast, staffing, supply, advisories):
    memory_bank.add_memory({
        "event_summary": forecast.get("notes", ""),
        "staffing_outcome": staffing,
        "supply_outcome": supply,
        "success_indicators": "pending - evaluation needed",
        "tags": ["festival" if "festival" in forecast.get("notes","").lower() else "general"]
    })
