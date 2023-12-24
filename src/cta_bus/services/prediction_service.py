from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cta_bus.ctatypes import BustimeResponseType

from cta_bus.models import ErrorObject, Prediction

from .utils import BaseService


class PredictionService(BaseService):
    @property
    def path(self: PredictionService) -> str:
        return "/getpredictions"

    def parse(self: PredictionService, data: BustimeResponseType) -> list[Prediction | ErrorObject] | list[ErrorObject]:
        error_objects = self.build_error_objects(data)
        bustime_response = data["bustime-response"]
        data_key = "prd"

        if data_key not in bustime_response:
            return error_objects

        predictions = [
            Prediction(
                timestamp=prd.get("tmstmp"),
                _type=prd.get("typ"),
                stop_id=prd.get("stpid"),
                stop_name=prd.get("stpnm"),
                vehicle_id=prd.get("vid"),
                distance_remaining=prd.get("dstp"),
                route_id=prd.get("rt"),
                route_display=prd.get("rtdd"),
                direction=prd.get("rtdir"),
                destination=prd.get("des"),
                predicted_time=prd.get("prdtm"),
                is_delayed=prd.get("dly"),
                dynamic_action_code=prd.get("dyn"),
                block_id=prd.get("tablockid"),
                trip_id=prd.get("tatripid"),
                original_trip_num=prd.get("origtatripno"),
                time_remaining=prd.get("prdctdn"),
                zone_name=prd.get("zone"),
                next_bus_after_service_gap=prd.get("nbus"),
                passenger_load=prd.get("psgld"),
                gtfs_stop_sequence=prd.get("gtfsseq"),
                scheduled_start_time_seconds=prd.get("stst"),
                scheduled_start_date=prd.get("stsd"),
                flag_stop_code=prd.get("flagstop"),
            ) for prd in bustime_response[data_key]
        ]

        return [*error_objects, *predictions]  # Return both errors and predictions, like in the JSON response.

    def get_list(self: PredictionService, params: dict) -> list[Prediction | ErrorObject] | list[ErrorObject]:
        data: BustimeResponseType = self.client.send(self.path, params).json()
        return self.parse(data)
