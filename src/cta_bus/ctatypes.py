from datetime import datetime
from typing import Literal, Union

BustimeResponseType = dict[str, dict[str, list[dict[str, Union[str, int, bool, list[dict], datetime]]]]]
""" Type for bustime API JSON response. """

SystemTimeResponseType = dict[str, dict[str, Union[list[dict[str, str]], str]]]
""" Type for system time JSON response. """

DirectionType = Literal[
    "Northbound",
    "Southbound",
    "Eastbound",
    "Westbound"
]
