from __future__ import annotations

from typing import TYPE_CHECKING, cast

from cta_bus.services.utils.base_service import BaseService

if TYPE_CHECKING:
    from cta_bus.ctatypes import BustimeResponseType

from cta_bus.models import ErrorObject, Pattern, Point


class PatternService(BaseService):
    @property
    def path(self: PatternService) -> str:
        return "/getpatterns"

    def parse(self: PatternService, data: BustimeResponseType) -> list[Pattern | ErrorObject] | list[ErrorObject]:
        error_objects = self.build_error_objects(data)
        bustime_response = data["bustime-response"]
        data_key = "ptr"

        if data_key not in bustime_response:
            return error_objects

        patterns = [
            Pattern(
                pattern_id=pattern.get("pid"),
                length=pattern.get("ln"),
                direction=pattern.get("rtdir"),
                points=[
                    Point(
                        position=point.get("seq"),
                        _type=point.get("typ"),
                        stop_id=point.get("stpid"),
                        stop_name=point.get("stpnm"),
                        distance_from_pattern=point.get("pdist"),
                        latitude=point.get("lat"),
                        longitude=point.get("lon"),
                    ) for point in cast(list[dict], pattern.get("pt"))  # Cast type explicitly.
                ]
            ) for pattern in bustime_response[data_key]
        ]

        return [*error_objects, *patterns]

    def get_list(self: PatternService, params: dict) -> list[Pattern | ErrorObject] | list[ErrorObject]:
        data: BustimeResponseType = self.client.send(self.path, params).json()
        return self.parse(data)
