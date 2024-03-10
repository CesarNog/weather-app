from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from typing import Union

from .weather_service import get_weather  # Ensure this import matches your project structure

app = FastAPI(title="Weather Forecast API", description="API for fetching weather forecasts", version="1.0")

@app.get("/", include_in_schema=False)
def docs_redirect():
    """
    Redirects the root URL to the API documentation.
    """
    return RedirectResponse(url='/docs')

@app.get("/temperature", summary="Get the predicted temperature", description="Returns the predicted temperature for a specific city.")
async def temperature(city: str = "Lisbon", days: int = 3, unit: Union[str, None] = None):
    """
    Endpoint to get the predicted temperature for a specific city.

    Parameters:
        city (str): The name of the city. Defaults to 'Lisbon'.
        days (int): The forecast period in days. Defaults to 3.
        unit (str, optional): The temperature unit ('C' or 'F'). Defaults to None, which will use the default unit in the weather service.

    Returns:
        JSON response containing the predicted temperature information.
    """
    return await get_weather(city, days, "temperature", unit or "C")  # Default unit to 'C' if not specified

@app.get("/rain", summary="Check if it will rain", description="Indicates whether it will rain in a specific city.")
async def rain(city: str = "Lisbon", days: int = 3):
    """
    Endpoint to check if it will rain in a specific city.

    Parameters:
        city (str): The name of the city. Defaults to 'Lisbon'.
        days (int): The forecast period in days. Defaults to 3.

    Returns:
        JSON response indicating whether it will rain in the specified city.
    """
    return await get_weather(city, days, "rain")
