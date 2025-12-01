# src/tools/roster_tool.py
import csv
from google.adk.tools import FunctionTool
from typing import Dict

class StaffRosterTool(FunctionTool):
    name = "staff_roster_tool"
    description = "Returns current baseline staffing counts (doctors/nurses/support)."

    def __call__(self) -> Dict[str, int]:
        result = {}
        with open("data/roster.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                result[row["role"]] = int(row["baseline_count"])
        return result
