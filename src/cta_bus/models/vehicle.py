from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime

from cta_bus.utils import to_datetime


@dataclass
class Vehicle:
    vehicle_id: str
    timestamp: datetime
    latitude: str
    longitude: str
    heading: str
    pattern_id: int
    linear_distance: int
    route_id: str
    destination: str
    is_delayed: bool
    speed: str | None
    block_id: str
    trip_id: str
    original_trip_num: str
    zone_name: str
    mode_of_transport: int
    passenger_load: str
    timepoint_id: str | None
    stop_sequence: str | None
    stop_status: str | None
    stop_id: str | None
    gtfs_stop_sequence: str | None
    scheduled_start_time_seconds: int
    scheduled_start_date: str

    def __post_init__(self: Vehicle) -> None:
        self.timestamp = to_datetime(self.timestamp)
