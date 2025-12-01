# src/tools/inventory_tool.py
from __future__ import annotations
import csv
from google.adk.tools import FunctionTool

def inventory_func() -> dict[str, int]:
    """Reads inventory levels of critical medical supplies."""
    result = {}
    with open("data/inventory.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            result[row["item"]] = int(row["units_in_stock"])
    return result

class InventoryTool(FunctionTool):
    """Reads inventory levels of critical medical supplies."""
    def __init__(self):
        super().__init__(func=inventory_func)
