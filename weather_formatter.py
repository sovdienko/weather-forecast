from weather_api_service import Weather


def format_weather(weather: Weather) -> str:
    """Formats Weather data into string"""
    return (f"{weather.city}, температура {weather.temperature}°C, "
            f"{weather.weather_type.value}\n"
            f"Схід сонця: {weather.sunrise.strftime('%H:%M')}\n"
            f"Захід сонця: {weather.sunset.strftime('%H:%M')}\n")


if __name__ == '__main__':
    from datetime import datetime
    from weather_api_service import WeatherType


    print(format_weather(Weather(
        temperature=15,
        weather_type=WeatherType.THUNDERSTORM,
        sunrise=datetime.fromisoformat("2022-12-14 07:00:00"),
        sunset=datetime.fromisoformat("2022-12-14 18:40:00"),
        city="Київ"
    )))
