# src/tools/pollution_api_tool.py
from __future__ import annotations
import requests
from google.adk.tools import FunctionTool
from typing import Any
from src.config import POLLUTION_API_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5/air_pollution/forecast"

def pollution_forecast_func(lat: float, lon: float) -> dict[str, Any]:
    """
    Gets the next 5 days of pollution forecast (PM2.5 & AQI)
    given latitude and longitude.
    """
    params = {
        "lat": lat,
        "lon": lon,
        "appid": POLLUTION_API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e), "data": None}

class PollutionForecastTool(FunctionTool):
    """Gets pollution forecast for a given location."""
    def __init__(self):
        super().__init__(func=pollution_forecast_func)
