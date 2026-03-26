from requests import get, RequestException
    
def get_coordinates_by_city(city: str):
    try:
        request = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        response = get(request, timeout=5)
        data = response.json()
        if data:
            return data["results"][0].get("latitude", "Coordinates not found"), data["results"][0].get("longitude", "Coordinates not found")
        return "Coordinates not found", "Coordinates not found"
    except RequestException as e:
        return f"Error fetching coordinates for city {city}: {e}"