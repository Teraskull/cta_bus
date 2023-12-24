from __future__ import annotations

from typing import TYPE_CHECKING

from cta_bus.services.utils.base_service import BaseService

if TYPE_CHECKING:
    from cta_bus.ctatypes import BustimeResponseType

from cta_bus.models import ErrorObject, Stop


class StopService(BaseService):
    @property
    def path(self: StopService) -> str:
        return "/getstops"

    def parse(self: StopService, data: BustimeResponseType) -> list[Stop | ErrorObject] | list[ErrorObject]:
        error_objects = self.build_error_objects(data)
        bustime_response = data["bustime-response"]
        data_key = "stops"

        if data_key not in bustime_response:
            return error_objects

        stops = [
            Stop(
                stop_id=stop.get("stpid"),
                stop_name=stop.get("stpnm"),
                latitude=stop.get("lat"),
                longitude=stop.get("lon"),
                detours_added_to=stop.get("dtradd"),
                detours_removed_from=stop.get("dtrrem"),
                gtfs_stop_sequence=stop.get("gtfsseq"),
                is_ada_accessible=stop.get("ada"),
            ) for stop in bustime_response[data_key]
        ]

        return [*error_objects, *stops]

    def get_list(self: StopService, params: dict) -> list[Stop | ErrorObject] | list[ErrorObject]:
        data: BustimeResponseType = self.client.send(self.path, params).json()
        return self.parse(data)
