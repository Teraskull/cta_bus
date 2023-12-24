from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cta_bus.ctatypes import BustimeResponseType

from cta_bus.models import Direction, ErrorObject

from .utils import BaseService


class DirectionService(BaseService):
    @property
    def path(self: DirectionService) -> str:
        return "/getdirections"

    def parse(self: DirectionService, data: BustimeResponseType) -> list[Direction | ErrorObject] | list[ErrorObject]:
        error_objects = self.build_error_objects(data)
        bustime_response = data["bustime-response"]
        data_key = "directions"

        if data_key not in bustime_response:
            return error_objects

        directions = [
            Direction(
                _id=direction.get("id"),
                name=direction.get("name"),
            ) for direction in bustime_response[data_key]
        ]

        return [*error_objects, *directions]

    def get_list(self: DirectionService, params: dict) -> list[Direction | ErrorObject] | list[ErrorObject]:
        data: BustimeResponseType = self.client.send(self.path, params).json()
        return self.parse(data)
