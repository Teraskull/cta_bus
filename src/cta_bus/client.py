from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import httpx

if TYPE_CHECKING:
    from .ctatypes import DirectionType
    from .models import Direction, ErrorObject, Pattern, Prediction, Route, Stop, SystemTime, Vehicle

from .constants import API_BASE
from .exceptions import InvalidParamError
from .services import (
    DirectionService,
    PatternService,
    PredictionService,
    RouteService,
    StopService,
    SystemTimeService,
    VehicleService,
)


class Client:
    def __init__(self: Client, api_key: str) -> None:
        self.base_url = API_BASE
        self.system_time = SystemTimeService(self)
        self.vehicles = VehicleService(self)
        self.routes = RouteService(self)
        self.directions = DirectionService(self)
        self.stops = StopService(self)
        self.patterns = PatternService(self)
        self.predictions = PredictionService(self)
        self.params = {"key": api_key, "format": "json"}

    def get_time(self: Client, unix_time: bool = False) -> list[SystemTime | ErrorObject] | list[ErrorObject]:
        params = {
            "unixTime": unix_time
        }

        return self.system_time.get_list(params)

    def get_vehicles(
            self: Client,
            route_id: str | list[str] | None = "",
            vehicle_id: str | list[str] | None = "",
            time_res: Literal["m", "s"] | None = None
    ) -> list[Vehicle | ErrorObject] | list[ErrorObject]:

        if route_id and vehicle_id:
            msg = "route_id and vehicle_id cannot both be provided"
            raise InvalidParamError(msg)

        if isinstance(route_id, list):
            route_id = ",".join(route_id)

        if isinstance(vehicle_id, list):
            vehicle_id = ",".join(vehicle_id)

        params = {
            k: v for k, v in {
                "rt": route_id,
                "vid": vehicle_id,
                "tmres": time_res,
            }.items() if v
        }

        return self.vehicles.get_list(params)

    def get_routes(self: Client) -> list[Route | ErrorObject] | list[ErrorObject]:
        params = {}
        return self.routes.get_list(params)

    def get_directions(self: Client, route_id: str) -> list[Direction | ErrorObject] | list[ErrorObject]:
        params = {
            "rt": route_id
        }

        return self.directions.get_list(params)

    def get_stops(
            self: Client,
            route_id: str | None = "",
            direction_id: DirectionType | None = None,
            stop_id: str | list[str] | None = ""
    ) -> list[Stop | ErrorObject] | list[ErrorObject]:

        if (route_id or direction_id) and stop_id:
            msg = "Only route_id and direction_id or stop_id are allowed"
            raise InvalidParamError(msg)

        if (route_id and not direction_id or direction_id and not route_id) and not stop_id:
            msg = "route_id and direction_id or stop_id are required"
            raise InvalidParamError(msg)

        if isinstance(stop_id, list):
            stop_id = ",".join(stop_id)

        params = {
            k: v for k, v in {
                "dir": direction_id,
                "rt": route_id,
                "stpid": stop_id,
            }.items() if v
        }

        return self.stops.get_list(params)

    def get_patterns(
            self: Client,
            pattern_id: str | list[str] | None = "",
            route_id: str | None = ""
    ) -> list[Pattern | ErrorObject] | list[ErrorObject]:

        if pattern_id and route_id:
            msg = "pattern_id and route_id cannot both be provided"
            raise InvalidParamError(msg)

        params = {
            k: v for k, v in {
                "pid": pattern_id,
                "rt": route_id,
            }.items() if v
        }

        # TODO: Add tests. Change underscored model variables to something else to prevent shadowing built-in types.

        return self.patterns.get_list(params)

    def get_predictions(
            self: Client,
            stop_id: str | list[str] | None = "",
            route_id: str | list[str] | None = None,
            vehicle_id: str | list[str] | None = "",
            max_results: int | None = None,
            time_res: Literal["m", "s"] | None = None
    ) -> list[Prediction | ErrorObject] | list[ErrorObject]:

        if stop_id and vehicle_id:
            msg = "stop_id and vehicle_id cannot both be provided"
            raise InvalidParamError(msg)

        if route_id and not stop_id:
            msg = "route_id is only available when stop_id is provided"
            raise InvalidParamError(msg)

        if isinstance(stop_id, list):
            stop_id = ",".join(stop_id)

        if isinstance(route_id, list):
            route_id = ",".join(route_id)

        if isinstance(vehicle_id, list):
            vehicle_id = ",".join(vehicle_id)

        params = {
            k: v for k, v in {
                "stpid": stop_id,
                "rt": route_id,
                "vid": vehicle_id,
                "top": max_results,
                "tmres": time_res,
            }.items() if v
        }

        return self.predictions.get_list(params)

    def send(self: Client, path: str, params: dict[str, str] | None = None) -> httpx.Response:
        """Send a request to the API with the given path and parameters."""
        all_params = self.params if params is None else {**self.params, **params}
        return httpx.get(f"{self.base_url}{path}", params=all_params)
