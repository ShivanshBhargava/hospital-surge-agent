# src/tools/hospital_data_tools.py
import csv
from datetime import datetime, timedelta

def read_recent_admissions(days: int = 14):
    """
    Reads the last N days of admissions from the CSV.
    Returns a list of dicts sorted newest → oldest.
    """
    rows = []
    with open("data/historical_admissions.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "date": row["date"],
                "total_admissions": int(row["total_admissions"]),
                "icu_admissions": int(row["icu_admissions"])
            })
    rows.sort(key=lambda x: x["date"], reverse=True)

    return rows[:days]
