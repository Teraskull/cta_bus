from dataclasses import dataclass

from cta_bus.ctatypes import DirectionType


@dataclass
class Direction:
    _id: DirectionType
    """
    This is the direction designator that should be used in other requests such as getpredictions.
    """

    name: DirectionType
    """
    This is the human-readable, locale-dependent name of the direction.
    """
