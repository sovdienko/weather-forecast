from typing import NamedTuple, List, Literal
# from geopy.geocoders import Nominatim
from subprocess import Popen, PIPE

import config
from exceptions import CantGetCoordinates


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


# One is an option to use Dict instead of NamedTuple
# def get_gps_coordinates() -> dict[Literal['latitude'] | Literal['longitude'], float]:

def get_coordinates() -> Coordinates:
    """Returns current GPS coordinates using Macbook GPS"""
    coordinates = _get_whereami_coordinates()
    return _round_coordinates(coordinates)


def _get_whereami_coordinates() -> Coordinates:
    whereami_output = _get_whereami_output()
    coordidates = _parse_coordinates(whereami_output)
    return coordidates


def _get_whereami_output() -> bytes:
    process = Popen(["whereami"], stdout=PIPE)
    output, err = process.communicate()
    exit_code = process.wait()
    if err is not None or exit_code != 0:
        raise CantGetCoordinates
    return output


def _parse_coordinates(whereami_output: bytes) -> Coordinates:
    try:
        output = whereami_output.decode().strip().lower().split("\n")
    except UnicodeError:
        raise CantGetCoordinates
    return Coordinates(
        latitude=_parse_coord(output, "latitude"),
        longitude=_parse_coord(output, "longitude")
    )


def _parse_coord(output: List[str], coord_type: Literal["latitude"] | Literal["longitude"]) ->float:
    for line in output:
        if line.startswith(f"{coord_type}:"):
            return _parse_float_coordinates(line.split()[1])
    else:
        raise CantGetCoordinates


def _parse_float_coordinates(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise CantGetCoordinates


def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    if not config.ROUNDING_COORDS:
        return coordinates
    return Coordinates(*map(lambda c: round(c, 1), [coordinates.latitude, coordinates.longitude]))


    # # address we need to geocode
    # loc = config.LOCATION_ADDR
    # # making an instance of Nominatim class
    # geolocator = Nominatim(user_agent="my_request")
    # # applying geocode method to get the location
    # location = geolocator.geocode(loc)
    # # printing address and coordinates
    # # print(location.address)
    # return Coordinates(location.latitude, location.longitude)


if __name__ == '__main__':
    (lat, long) = get_coordinates()
    print(lat)
    print(long)
