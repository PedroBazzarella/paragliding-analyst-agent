from requests import get, RequestException
from langchain.tools import tool

from utils.coord_city import get_coordinates_by_city
from utils.get_weather_by_code import get_weather_by_code

def get_weather_city(city: str):
    try:
        lat, lon = get_coordinates_by_city(city)
        request = f"""https://api.open-meteo.com/v1/forecast?timezone=auto&latitude={lat}&longitude={lon}&current=weather_code,temperature_2m,relative_humidity_2m,is_day"""
        response = get(request, timeout=5)
        data = response.json()
        if data:
            data = data["current"]
            data["city"] = city
            data["is_day"] = bool(data["is_day"])
            data["weather"] = get_weather_by_code(data["weather_code"], data["is_day"])

            del data["weather_code"]
            del data["interval"]

        return data

    except RequestException as e:
        return f"Error fetching weather for {city}: {e}"
    
@tool
def get_weather(city: str):
    """Gets the general weather info for a specific city. Calls when the user wants the current weather information. Returns last update timestamp, temperature, humidity and weather condition for given city."""
    return get_weather_city(city)