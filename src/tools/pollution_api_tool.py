# src/tools/pollution_api_tool.py
import requests
from google.adk.tools import FunctionTool
from typing import Dict, Any
from src.config import POLLUTION_API_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5/air_pollution/forecast"

class PollutionForecastTool(FunctionTool):
    name = "pollution_forecast_tool"
    description = (
        "Gets the next 5 days of pollution forecast (PM2.5 & AQI) "
        "given latitude and longitude."
    )

    def __call__(self, lat: float, lon: float) -> Dict[str, Any]:
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
