# weather1.py
import requests

API_KEY = "a7711edb7f3349e1a85124505252811"
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def get_weather(city):
    """
    Returns (info_dict, error_message)
    info_dict = {
        city, country, time, temp, humidity, condition, wind_kph
    }
    If error, info_dict = None and error_message is a string.
    """
    params = {
        "key": API_KEY,
        "q": city
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()

        if "error" in data:
            return None, data["error"]["message"]

        location = data["location"]
        current = data["current"]

        info = {
            "city": location["name"],
            "country": location["country"],
            "time": location["localtime"],
            "temp": current["temp_c"],
            "humidity": current["humidity"],
            "condition": current["condition"]["text"],
            "wind_kph": current["wind_kph"]
        }
        return info, None

    except requests.exceptions.RequestException as e:
        return None, f"Network error: {e}"


# Optional: keep console test, but not required for Flask
if __name__ == "__main__":
    city = input("Enter city for test: ")
    info, err = get_weather(city)
    if err:
        print("Error:", err)
    else:
        print(info)
