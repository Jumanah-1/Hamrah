import json
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import URLError

from fastapi import FastAPI, HTTPException

from backend.rainfall import process_rainfall

from pydantic import BaseModel, Field
from backend.risk_model import calculate_road_risk

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

class RiskRequest(BaseModel):
    road_id: str
    rain_6h_mm: float = Field(ge=0)
    slope_percent: float = Field(ge=0)
    upstream_area_km2: float = Field(ge=0)
    impervious_fraction: float = Field(ge=0, le=1)
    is_tunnel: bool


@app.post("/api/risk/preview")
def preview_road_risk(request: RiskRequest):

    result = calculate_road_risk(
        rain_6h_mm=request.rain_6h_mm,
        slope_percent=request.slope_percent,
        upstream_area_km2=request.upstream_area_km2,
        impervious_fraction=request.impervious_fraction,
        is_tunnel=request.is_tunnel
    )

    return {
        "road_id": request.road_id,
        "risk_score": result["risk_score"],
        "risk_level": result["risk_level"],
        "mode": "prototype"
    }