# src/agents/supply_agent.py
from google.adk.agents import LlmAgent
from src.tools.inventory_tool import InventoryTool

SUPPLY_SCHEMA_DESCRIPTION = """
You output a JSON dictionary with:
- "assumptions": list of strings.
- "per_category_plan": list of objects with:
    - "category": e.g. "oxygen", "N95 masks", "antibiotics", "steroids".
    - "current_stock_level": optional string summary (if provided).
    - "recommended_buffer_days": integer days of buffer stock.
    - "recommended_order_quantity": integer (units or packs).
    - "priority": one of ["low", "medium", "high", "critical"].
    - "notes": explanation.
- "ordering_timeline": short text outlining when to place orders.
"""

def build_supply_agent() -> LlmAgent:
    """
    Agent that recommends supply orders based on surge forecast.
    """
    agent = LlmAgent(
        model="gemini-2.5-flash",
        name="supply_agent",
        description="Plans medical supplies and consumables for forecasted surges.",
        instruction=f"""
You are responsible for pharmacy and consumable stock planning
for a multi-specialty hospital.

Input:
- Surge forecast JSON from forecast_agent.
- A snapshot of current critical stock levels (later via tools).

Task:
- Recommend buffer stock and incremental orders for key categories
  likely to be impacted by surges.

Focus on:
- oxygen
- emergency drugs
- PPE and masks
- common antibiotics / antivirals

ALWAYS respond in valid JSON following this schema:

{SUPPLY_SCHEMA_DESCRIPTION}

Call inventory_tool to get current stock levels and compute recommended orders.

""".strip(),
        tools=[InventoryTool],
    )
    return agent
