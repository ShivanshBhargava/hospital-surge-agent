# src/agents/orchestrator.py

from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool  # You can also add CodeExecutionTool if you want

from .forecast_agent import build_forecast_agent
from .staffing_agent import build_staffing_agent
from .supply_agent import build_supply_agent
from .advisory_agent import build_advisory_agent

from src.memory.session_store import SessionStore
from src.memory.memory_bank import MemoryBank
from src.observability.logger import logger

# Session + long-term memory instances (shared for orchestrations)
session = SessionStore()
memory_bank = MemoryBank()


def build_orchestrator_agent() -> LlmAgent:
    """
    Top-level orchestrator agent.

    This agent coordinates the multi-agent workflow:
      - Forecasts surges
      - Plans staffing
      - Plans supplies
      - Generates patient advisories

    It delegates to specialist agents via AgentTool.
    """
    forecast_agent = build_forecast_agent()
    staffing_agent = build_staffing_agent()
    supply_agent = build_supply_agent()
    advisory_agent = build_advisory_agent()

    logger.info("Building hospital orchestrator agent")

    orchestrator = LlmAgent(
        model="gemini-2.0-flash",
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

LONG-TERM MEMORY
If relevant past surge events exist in long-term memory, incorporate them.
Memory entries include:
- event_summary
- staffing_outcome
- supply_outcome
- success_indicators
- tags

Use them ONLY as guidance, not as deterministic rules.

Before calling any specialist agent, conceptually perform a MEMORY_RETRIEVAL step.
The runtime will provide you related memory snippets in the context.
Use them only to adjust your plan, for example:
- learn from past festival surges
- avoid repeating past under-staffing mistakes
- adjust supply buffers if previous stockouts occurred

TOOLS
You have access to these tools (as AgentTools):
- forecast_agent: produces surge forecasts.
- staffing_agent: produces staffing plans.
- supply_agent: produces supply / stock plans.
- advisory_agent: produces patient advisory messages.

Always call these tools rather than inventing deeply detailed plans yourself.
        """.strip(),
        tools=[
            AgentTool(agent=forecast_agent),
            AgentTool(agent=staffing_agent),
            AgentTool(agent=supply_agent),
            AgentTool(agent=advisory_agent),
            # You can add CodeExecutionTool() here later if needed.
        ],
    )

    return orchestrator


def remember_outcome(forecast, staffing, supply, advisories) -> None:
    """
    Store the outcome of a completed orchestration cycle into long-term memory.

    This is intended to be called by the runtime AFTER the orchestrator and
    all specialist agents have produced their outputs.
    """
    try:
        notes = forecast.get("notes", "") if isinstance(forecast, dict) else ""
        tags = []
        if "festival" in notes.lower():
            tags.append("festival")
        if not tags:
            tags.append("general")

        entry = {
            "event_summary": notes,
            "staffing_outcome": staffing,
            "supply_outcome": supply,
            "success_indicators": "pending - evaluation needed",
            "tags": tags,
        }
        memory_bank.add_memory(entry)
        logger.info("Saved outcome to memory_bank: %s", entry)
    except Exception as e:
        logger.error("Failed to save outcome to memory_bank: %s", e)
