from requests import get, RequestException
from langchain.tools import tool

from utils.coord_city import get_coordinates_by_city
from utils.get_weather_by_code import get_weather_by_code

def get_paragliding_conditions_city(city: str):
    try:
        lat, lon = get_coordinates_by_city(city)
        request = f"""https://api.open-meteo.com/v1/forecast?timezone=auto&latitude={lat}&longitude={lon}&daily=weather_code,precipitation_sum,precipitation_hours,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,rain_sum,showers_sum,snowfall_sum&current=temperature_2m,relative_humidity_2m,is_day,precipitation,rain,surface_pressure,pressure_msl,cloud_cover,weather_code,wind_direction_10m,wind_gusts_10m,wind_speed_10m&past_days=2&forecast_days=1"""
        response = get(request, timeout=5)
        data = response.json()
        if data:
            data["city"] = city
            data["current"]["is_day"] = bool(data["current"]["is_day"])
            data["current"]["weather"] = get_weather_by_code(data["current"]["weather_code"], data["current"]["is_day"])

            del data["current"]["weather_code"]
            del data["current"]["interval"]
        return data

    except RequestException as e:
        return f"Error fetching weather for {city}: {e}"
    
@tool
def get_paragliding_conditions(city: str):
    """Gets the paragliding conditions info for a specific city. Calls when the user wants paragliding conditions. For current weather, returns temperature, humidity, precipitation, rain, surface pressure, cloud cover, and wind conditions. Returns daily weather forecasts for yesterday, today and tomorrow, this can be useful for checking rain probabilities."""
    return get_paragliding_conditions_city(city)