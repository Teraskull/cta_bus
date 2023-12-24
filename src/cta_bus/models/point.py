from dataclasses import dataclass
from typing import Literal


@dataclass
class Point:
    position: int
    _type: Literal["S", "W"]
    stop_id: str
    stop_name: str
    distance_from_pattern: float
    latitude: float
    longitude: float
