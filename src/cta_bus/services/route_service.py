from __future__ import annotations

from typing import TYPE_CHECKING

from cta_bus.services.utils.base_service import BaseService

if TYPE_CHECKING:
    from cta_bus.ctatypes import BustimeResponseType

from cta_bus.models import ErrorObject, Route


class RouteService(BaseService):
    @property
    def path(self: RouteService) -> str:
        return "/getroutes"

    def parse(self: RouteService, data: BustimeResponseType) -> list[Route | ErrorObject] | list[ErrorObject]:
        error_objects = self.build_error_objects(data)
        bustime_response = data["bustime-response"]
        data_key = "routes"

        if data_key not in bustime_response:
            return error_objects

        routes = [
            Route(
                route_id=route.get("rt"),
                route_name=route.get("rtnm"),
                route_color=route.get("rtclr"),
                route_display=route.get("rtdd"),
            ) for route in bustime_response[data_key]
        ]

        return [*error_objects, *routes]

    def get_list(self: RouteService, params: dict) -> list[Route | ErrorObject] | list[ErrorObject]:
        data: BustimeResponseType = self.client.send(self.path, params).json()
        return self.parse(data)
