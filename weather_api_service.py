from enum import Enum
from datetime import datetime
from typing import NamedTuple, Literal
import json
from json.decoder import JSONDecodeError

import ssl
import urllib.request
from urllib.error import URLError

import config
from coordinates import Coordinates
from exceptions import ApiServiceError

Celsius = int


class WeatherType(Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Поморозь"
    RAIN = "Дощ"
    SNOW = "Сніг"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Хмарно"


class Weather(NamedTuple):
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str


# def what_should_i_do(weather_type: WeatherType):
#     match weather_type:
#         case WeatherType.RAIN | WeatherType.THUNDERSTORM:
#             print('Sit at home')
#         case WeatherType.CLEAR:
#             print('Good weather')
#         case _:
#             print('So so')
#
#
# what_should_i_do(weather_type=WeatherType.FOG)


def get_weather(coordinates: Coordinates) -> Weather:
    """Request weather in OpenWeather API and returns it"""
    openweather_response = _get_openweather_response(latitude=coordinates.latitude, longitude=coordinates.longitude)
    weather = _parse_openweather_response(openweather_response)
    return weather


def _get_openweather_response(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.OPENWEATHER_URL.format(latitude=latitude, longitude=longitude)
    try:
        return urllib.request.urlopen(url)
    except URLError:
        raise ApiServiceError


def _parse_openweather_response(openweather_response: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_response)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(
        temperature=_parse_temperature(openweather_dict),
        weather_type=_parse_weather_type(openweather_dict),
        sunrise=_parse_sun_time(openweather_dict, "sunrise"),
        sunset=_parse_sun_time(openweather_dict, "sunset"),
        city=_parse_city(openweather_dict)
    )


def _parse_temperature(openweather_dict: dict) -> Celsius:
    return round(openweather_dict["main"]["temp"])


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict["weather"][0]["id"])
    except (IndexError, KeyError):
        raise ApiServiceError

    weather_type = {
        '1': WeatherType.THUNDERSTORM,
        '3': WeatherType.DRIZZLE,
        '5': WeatherType.RAIN,
        '6': WeatherType.SNOW,
        '7': WeatherType.FOG,
        '800': WeatherType.CLEAR,
        '80': WeatherType.CLOUDS
    }

    for _id, _weather_type in weather_type.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError


def _parse_sun_time(openweather_dict: dict,
                    time: Literal['sunrise'] | Literal['sunset']) -> datetime:
    return datetime.fromtimestamp(openweather_dict['sys'][time])


def _parse_city(openweather_dict: dict) -> str:
    return openweather_dict['name']


if __name__ == '__main__':
    print(get_weather(Coordinates(latitude=50.34912109375, longitude=30.477296071816152)))
