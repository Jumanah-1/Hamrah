import json
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import URLError

from fastapi import FastAPI, HTTPException

from backend.rainfall import process_rainfall

app = FastAPI(
    title="Hamrah API",
    description="Flood Risk Prediction and Smart Routing for Jeddah",
    version="1.0.0"
)


# API 1: Health Check
@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "project": "Hamrah",
        "message": "Backend is running successfully"
    }


# API 2: Jeddah Rainfall Forecast
@app.get("/api/weather")
def get_weather():

    params = {
        "latitude": 21.5433,
        "longitude": 39.1728,
        "hourly": "precipitation,precipitation_probability",
        "forecast_hours": 48,
        "timezone": "Asia/Riyadh"
    }

    url = "https://api.open-meteo.com/v1/forecast?" + urlencode(params)

    try:
        with urlopen(url, timeout=15) as response:
            data = json.load(response)

    except (URLError, TimeoutError, ValueError) as error:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch weather data"
        ) from error

    return {
        "city": "Jeddah",
        "source": "Open-Meteo",
        "timezone": data.get("timezone"),
        "units": data.get("hourly_units"),
        "hourly": data.get("hourly"),
        "rainfall_analysis": process_rainfall(data["hourly"])
    }