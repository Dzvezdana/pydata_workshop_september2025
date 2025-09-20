from dapr_agents import tool
from pydantic import BaseModel, Field
import requests


class GetWeatherSchema(BaseModel):
    location: str = Field(description="location to get weather for")

@tool(args_model=GetWeatherSchema)
def get_weather(location: str) -> str:
    """Get weather information based on location."""
    # Use Geocode API to get coordinates for the city name 
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}"
    geo_resp = requests.get(geo_url).json()

    if not geo_resp.get("results"):
        return f"Could not find coordinates for {location}"

    lat = geo_resp["results"][0]["latitude"]
    lon = geo_resp["results"][0]["longitude"]

    # Get the current weather from Open-Meteo API
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current_weather=true"
    )
    weather_resp = requests.get(weather_url).json()
    current = weather_resp.get("current_weather")

    if not current:
        return f"No weather data available for {location}"

    temperature = current["temperature"]
    return f"{location}: {temperature}C."


tools = [get_weather]
