from dataclasses import dataclass


@dataclass
class Stop:
    stop_id: str
    stop_name: str
    latitude: float
    longitude: float
    detours_added_to: list
    detours_removed_from: list
    gtfs_stop_sequence: str
    is_ada_accessible: bool
