import requests

from config import OPENWEATHER_API_KEY


# ============================================================
# OPENWEATHER SETTINGS
# ============================================================

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

REQUEST_TIMEOUT = 10


# ============================================================
# WEATHER API
# ============================================================

def get_weather(city):
    """
    Get current weather information for a city.

    Returns a dictionary so the Streamlit page can safely
    handle both successful and failed requests.
    """

    city = str(city).strip()

    if not city:
        return {
            "success": False,
            "message": "Please enter a city name.",
        }

    if not OPENWEATHER_API_KEY:
        return {
            "success": False,
            "message": (
                "OpenWeather API key is missing. "
                "Add OPENWEATHER_API_KEY to your .env file."
            ),
        }

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )

        # Invalid API key
        if response.status_code == 401:

            return {
                "success": False,
                "message": (
                    "OpenWeather API key is invalid. "
                    "Please check OPENWEATHER_API_KEY."
                ),
            }

        # City not found
        if response.status_code == 404:

            return {
                "success": False,
                "message": (
                    f"Could not find weather information "
                    f"for '{city}'. Please check the city name."
                ),
            }

        # Rate limit
        if response.status_code == 429:

            return {
                "success": False,
                "message": (
                    "Weather API request limit reached. "
                    "Please try again later."
                ),
            }

        response.raise_for_status()

        data = response.json()

        main = data.get(
            "main",
            {},
        )

        wind = data.get(
            "wind",
            {},
        )

        weather_list = data.get(
            "weather",
            [],
        )

        weather = (
            weather_list[0]
            if weather_list
            else {}
        )

        return {
            "success": True,

            "city": data.get(
                "name",
                city,
            ),

            "country": data.get(
                "sys",
                {},
            ).get(
                "country",
                "",
            ),

            "temperature": main.get(
                "temp",
                "N/A",
            ),

            "feels_like": main.get(
                "feels_like",
                "N/A",
            ),

            "humidity": main.get(
                "humidity",
                "N/A",
            ),

            "pressure": main.get(
                "pressure",
                "N/A",
            ),

            "wind_speed": wind.get(
                "speed",
                "N/A",
            ),

            "description": weather.get(
                "description",
                "Unknown",
            ),

            "icon": weather.get(
                "icon",
                "",
            ),

            "main_condition": weather.get(
                "main",
                "Unknown",
            ),
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "message": (
                "Weather service took too long to respond. "
                "Please try again."
            ),
        }

    except requests.exceptions.ConnectionError:

        return {
            "success": False,
            "message": (
                "Could not connect to the weather service. "
                "Please check your internet connection."
            ),
        }

    except requests.exceptions.RequestException as error:

        print(
            "Weather API Error:",
            error,
        )

        return {
            "success": False,
            "message": (
                "Unable to retrieve weather information "
                "right now."
            ),
        }

    except ValueError:

        return {
            "success": False,
            "message": (
                "The weather service returned an invalid response."
            ),
        }

    except Exception as error:

        print(
            "Unexpected Weather Error:",
            error,
        )

        return {
            "success": False,
            "message": (
                "An unexpected error occurred while "
                "getting weather information."
            ),
        }


# ============================================================
# FARMING ADVICE
# ============================================================

def farming_advice(
    temperature,
    humidity,
):
    """
    Generate simple general farming advice from weather
    conditions.

    This is general guidance, not a crop-specific treatment
    recommendation.
    """

    try:

        temperature = float(
            temperature
        )

        humidity = float(
            humidity
        )

    except (
        TypeError,
        ValueError,
    ):

        return (
            "Monitor local weather conditions and "
            "follow crop-specific agricultural guidance."
        )

    advice = []

    # --------------------------------------------------------
    # Temperature
    # --------------------------------------------------------

    if temperature >= 35:

        advice.append(
            "High temperature: monitor crops for heat stress "
            "and maintain appropriate irrigation."
        )

    elif temperature >= 30:

        advice.append(
            "Warm conditions: monitor soil moisture "
            "and crop water requirements."
        )

    elif temperature <= 15:

        advice.append(
            "Cool conditions: monitor temperature-sensitive "
            "crops for cold stress."
        )

    else:

        advice.append(
            "Temperature is within a moderate range "
            "for many crops."
        )

    # --------------------------------------------------------
    # Humidity
    # --------------------------------------------------------

    if humidity >= 80:

        advice.append(
            "High humidity: monitor crops closely for "
            "fungal disease symptoms and maintain good airflow."
        )

    elif humidity <= 35:

        advice.append(
            "Low humidity: monitor crops and soil moisture "
            "carefully, especially during hot weather."
        )

    else:

        advice.append(
            "Humidity is at a moderate level."
        )

    # --------------------------------------------------------
    # Combined Recommendation
    # --------------------------------------------------------

    return " ".join(
        advice
    )


# ============================================================
# OPTIONAL SIMPLE FORECAST HELPERS
# ============================================================

def is_rainy_condition(weather_result):
    """
    Return True when the current weather description indicates
    rain or a storm.
    """

    if not weather_result:
        return False

    description = str(
        weather_result.get(
            "description",
            "",
        )
    ).lower()

    keywords = (
        "rain",
        "drizzle",
        "thunderstorm",
        "storm",
    )

    return any(
        keyword in description
        for keyword in keywords
    )


def weather_summary(weather_result):
    """
    Create a short human-readable weather summary.
    """

    if not weather_result:
        return (
            "Weather information is unavailable."
        )

    if not weather_result.get(
        "success",
        False,
    ):
        return weather_result.get(
            "message",
            "Weather information is unavailable.",
        )

    city = weather_result.get(
        "city",
        "Unknown location",
    )

    temperature = weather_result.get(
        "temperature",
        "N/A",
    )

    humidity = weather_result.get(
        "humidity",
        "N/A",
    )

    description = weather_result.get(
        "description",
        "unknown conditions",
    )

    return (
        f"Weather in {city}: "
        f"{temperature}°C, "
        f"{humidity}% humidity, "
        f"{description}."
    )