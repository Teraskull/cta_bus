from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cta_bus.ctatypes import BustimeResponseType

from cta_bus.models import ErrorObject, Vehicle

from .utils import BaseService


class VehicleService(BaseService):
    @property
    def path(self: VehicleService) -> str:
        return "/getvehicles"

    def parse(self: VehicleService, data: BustimeResponseType) -> list[Vehicle | ErrorObject] | list[ErrorObject]:
        error_objects = self.build_error_objects(data)
        bustime_response = data["bustime-response"]
        data_key = "vehicles"

        if data_key not in bustime_response:
            return error_objects

        vehicles = [
            Vehicle(
                vehicle_id=vehicle.get("vid"),
                timestamp=vehicle.get("tmstmp"),
                latitude=vehicle.get("lat"),
                longitude=vehicle.get("lon"),
                heading=vehicle.get("hdg"),
                pattern_id=vehicle.get("pid"),
                linear_distance=vehicle.get("pdist"),
                route_id=vehicle.get("rt"),
                destination=vehicle.get("des"),
                is_delayed=vehicle.get("dly"),
                speed=vehicle.get("spd"),
                block_id=vehicle.get("tablockid"),
                trip_id=vehicle.get("tatripid"),
                original_trip_num=vehicle.get("origtatripno"),
                zone_name=vehicle.get("zone"),
                mode_of_transport=vehicle.get("mode"),
                passenger_load=vehicle.get("psgld"),
                timepoint_id=vehicle.get("timepointid"),
                stop_sequence=vehicle.get("sequence"),
                stop_status=vehicle.get("stopstatus"),
                stop_id=vehicle.get("stopid"),
                gtfs_stop_sequence=vehicle.get("gtfsseq"),
                scheduled_start_time_seconds=vehicle.get("stst"),
                scheduled_start_date=vehicle.get("stsd"),
            ) for vehicle in bustime_response[data_key]
        ]

        return [*error_objects, *vehicles]

    def get_list(self: VehicleService, params: dict) -> list[Vehicle | ErrorObject] | list[ErrorObject]:
        data: BustimeResponseType = self.client.send(self.path, params).json()
        return self.parse(data)
