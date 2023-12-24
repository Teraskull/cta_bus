from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cta_bus.ctatypes import SystemTimeResponseType

from cta_bus.models import ErrorObject, SystemTime

from .utils import BaseService


class SystemTimeService(BaseService):
    @property
    def path(self: SystemTimeService) -> str:
        return "/gettime"

    def parse(
            self: SystemTimeService,
            data: SystemTimeResponseType
    ) -> list[SystemTime | ErrorObject] | list[ErrorObject]:
        error_objects = self.build_error_objects(data)
        bustime_response = data["bustime-response"]
        data_key = "tm"

        if data_key not in bustime_response:
            return error_objects

        system_time = SystemTime(
            timestamp=bustime_response.get(data_key),
        )

        return [*error_objects, system_time]   # SystemTime is always a single element.

    def get_list(self: SystemTimeService, params: dict) -> list[SystemTime | ErrorObject] | list[ErrorObject]:
        data: SystemTimeResponseType = self.client.send(self.path, params).json()
        return self.parse(data)
