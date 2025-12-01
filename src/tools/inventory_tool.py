# src/tools/inventory_tool.py
import csv
from google.adk.tools import FunctionTool
from typing import Dict

class InventoryTool(FunctionTool):
    name = "inventory_tool"
    description = "Reads inventory levels of critical medical supplies."

    def __call__(self) -> Dict[str, int]:
        result = {}
        with open("data/inventory.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                result[row["item"]] = int(row["units_in_stock"])
        return result
