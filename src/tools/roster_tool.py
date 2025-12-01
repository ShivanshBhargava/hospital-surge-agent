# src/tools/roster_tool.py
from __future__ import annotations
import csv
from google.adk.tools import FunctionTool

def staff_roster_func() -> dict[str, int]:
    """Returns current baseline staffing counts (doctors/nurses/support)."""
    result = {}
    with open("data/roster.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            result[row["role"]] = int(row["baseline_count"])
    return result

class StaffRosterTool(FunctionTool):
    """Returns current baseline staffing counts (doctors/nurses/support)."""
    def __init__(self):
        super().__init__(func=staff_roster_func)
