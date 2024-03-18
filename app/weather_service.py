import os
from typing import Any, Callable, Dict, Union
from fastapi import HTTPException
from pydantic_settings import BaseSettings
import httpx
import logging

# Configuration management with Pydantic
class Settings(BaseSettings):
    weather_api_key: str = os.getenv("WEATHER_API_KEY")
    base_url: str = "http://api.weatherapi.com/v1/forecast.json"

    class Config:
        env_file = ".env"

settings = Settings()

# Custom asynchronous context manager for httpx.AsyncClient
class AsyncHTTPClient:
    def __init__(self, *args, **kwargs):
        self.client = httpx.AsyncClient(*args, **kwargs)

    async def __aenter__(self):
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

# Utility function for parameter validation
def validate_parameters(unit: str, days: int):
    valid_units = {"C", "F"}
    if unit not in valid_units:
        raise HTTPException(status_code=400, detail="Invalid unit parameter. Choose 'C' or 'F'.")
    if not 1 <= days <= 10:
        raise HTTPException(status_code=400, detail="The 'days' parameter must be between 1 and 10.")

# Asynchronous function to fetch weather data
async def get_weather(city: str, days: int, endpoint: str, unit: str = "C") -> Dict[str, Any]:
    validate_parameters(unit, days)
    async with AsyncHTTPClient() as client:
        response = await client.get(settings.base_url, params={"key": settings.weather_api_key, "q": city, "days": days, "aqi": "no", "alerts": "no"})
    data = response.json()

    # Advanced error handling
    if 'error' in data:
        error_message = data["error"]["message"]
        logging.error(f"Weather API error: {error_message}")
        raise HTTPException(status_code=404, detail=error_message)

    try:
        forecast_day = data["forecast"]["forecastday"][days - 1]
    except (KeyError, IndexError) as e:
        logging.error(f"Data parsing error: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Forecast data for {days} days ahead is not available.")

    return parameter_handlers[endpoint](forecast_day, city, days, unit)

# Handlers for different weather parameters
parameter_handlers: Dict[str, Callable[..., Dict[str, Union[str, int, float]]]] = {
    "temperature": lambda day, city, days, unit: handle_temperature(day, city, days, unit),
    "rain": lambda day, city, days, _: handle_rain(day, city, days),
}

def handle_temperature(forecast_day: Dict[str, Any], city: str, days: int, unit: str) -> Dict[str, str]:
    temp_keys = {"avgtemp_c": "avgtemp_c", "avgtemp_f": "avgtemp_f"}
    temp_key = temp_keys[f"avgtemp_{unit.lower()}"]
    avg_temp = forecast_day["day"].get(temp_key, "N/A")
    min_temp = forecast_day["day"].get("mintemp_{}".format(unit.lower()), "N/A")
    max_temp = forecast_day["day"].get("maxtemp_{}".format(unit.lower()), "N/A")
    return {
        "message": f"The average temperature in {city} in {days} days will be {avg_temp}°{unit}. The minimum temperature will be {min_temp}°{unit} and the maximum {max_temp}°{unit}."
    }

def handle_rain(forecast_day: Dict[str, Any], city: str, days: int) -> Dict[str, str]:
    rain_mm = forecast_day["day"].get("totalprecip_mm", 0)
    rain_message = "is expected to rain" if rain_mm > 0 else "is not expected to rain"
    return {"message": f"It {rain_message} in {city} in {days} days."}
