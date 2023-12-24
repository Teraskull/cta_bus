from dataclasses import dataclass

from cta_bus.ctatypes import DirectionType

from .point import Point


@dataclass
class Pattern:
    pattern_id: str
    length: float
    direction: DirectionType
    points: list[Point]

    # detour_id: str  # /getdetours is not really used by CTA.
    # detour_points: list[Point]
