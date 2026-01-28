from flask import Flask, render_template, request
import requests

# Weather API configuration
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

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    info = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if not city:
            error = "Please enter a city name."
        else:
            info, error = get_weather(city)

    return render_template("index.html", info=info, error=error)

if __name__ == "__main__":
    app.run(debug=True)
