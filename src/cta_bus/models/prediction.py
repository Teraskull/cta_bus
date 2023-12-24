from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from datetime import datetime

    from cta_bus.ctatypes import DirectionType

from cta_bus.utils import to_datetime


@dataclass
class Prediction:
    timestamp: datetime
    """
    Date and time (local) the prediction was generated.
    Date and time is represented based on the tmres parameter.
    """

    _type: Literal["A", "D"]
    """
    Type of prediction.
    `A` for an arrival prediction (prediction of when the vehicle will arrive at this stop).
    `D` for a departure prediction (prediction of when the vehicle will depart this stop, if applicable).
    Predictions made for first stops of a route or layovers are examples of departure predictions.
    """

    stop_id: str
    """
    Unique identifier representing the stop for which this prediction was generated.
    """

    stop_name: str
    """
    Display name of the stop for which this prediction was generated.
    """

    vehicle_id: str
    """
    Unique ID of the vehicle for which this prediction was generated.
    """

    distance_remaining: int
    """
    Linear distance (feet) left to be traveled by the vehicle
    before it reaches the stop associated with this prediction.
    """

    route_id: str
    """
    Alphanumeric designator of the route (ex. “20” or “X20”) for which this prediction was generated.
    """

    route_display: str
    """
    Language-specific route designator meant for display.
    """

    direction: DirectionType
    """
    Direction of travel of the route associated with this prediction (ex. “INBOUND”).
    This matches the direction id seen in the getdirections call.
    """

    destination: str
    """
    Final destination of the vehicle associated with this prediction.
    """

    predicted_time: datetime
    """
    Predicted date and time (local) of a vehicle's arrival or departure to the stop associated with this prediction.
    Date and time is represented based on the tmres parameter.
    """

    is_delayed: bool
    """
    `True` if the vehicle is delayed.
    In version 3 this element is always present.
    This is not used by RTPI feeds. (Not set by CAD dynamic action `unknown delay`)
    """

    dynamic_action_code: int
    """
    The dynamic action type affecting this prediction.

    `0` - None
        No change.
    `1` - Canceled
        The event or trip has been canceled.
    `2` - Reassigned
        The event or trip has been moved to a different work (to be handled by a different vehicle or operator).
    `3` - Shifted
        The time of this event, or the entire trip, has been moved.
    `4` - Expressed
        The event is “drop-off only” and will not stop to pick up passengers.
    `6` - Stops Affected
        This trip has events that are affected by Disruption Management changes, but the trip itself is not affected.
    `8` - New Trip
        This trip was created dynamically and does not appear in the TA schedule.
    `9` - Partial Trip
        This trip has been split, and this part of the split is using the original trip identifier(s).
    `10` - Partial Trip New
        This trip has been split, and this part of the split has been assigned a new trip identifier(s).
    `12` - Delayed Cancel
        This event or trip has been marked as canceled, but the cancellation should not be shown to the public.
    `13` - Added Stop
        This event has been added to the trip. It was not originally scheduled.
    `14` - Unknown Delay
        This trip has been affected by a delay.
    `15` - Unknown Delay New
        This trip, which was created dynamically, has been affected by a delay.
    `16` - Invalidated Trip
        This trip has been invalidated. Predictions for it should not be shown to the public.
    `17` - Invalidated Trip New
        This trip, which was created dynamically, has been invalidated.
        Predictions for it should not be shown to the public.
    `18` - Cancelled Trip New
        This trip, which was created dynamically, has been canceled.
    `19` - Stops Affected New
        This trip, which was created dynamically, has events that are affected
        by Disruption Management changes, but the trip itself is not affected.
    """

    block_id: str
    """
    TA's version of the scheduled block identifier for the work currently being performed by the vehicle.
    """

    trip_id: str
    """
    TA's version of the scheduled trip identifier for the vehicle's current trip.
    """

    original_trip_num: str
    """
    Trip ID defined by the TA scheduling system.
    """

    time_remaining: str
    """
    This is the time left, in minutes, until the bus arrives at this stop.
    """

    zone_name: str
    """
    The zone name if the vehicle has entered a defined zones, otherwise blank.
    This is not used by RTPI feeds.
    """

    gtfs_stop_sequence: str | None
    """
    Contains the GTFS stop sequence of the stop for which this prediction was generated.
    Only included if the BusTime property `developer.api.include.gtfsseq` is true.
    """

    passenger_load: str
    """
    String representing the ratio of the current passenger count to the vehicle's total capacity.
    Possible values include `FULL`, `HALF_EMPTY`, `EMPTY` and `N/A`.
    Ratios for `FULL`, `HALF_EMPTY` and `EMPTY` are determined by the transit agency.
    `N/A` indicates that the passenger load is unknown.
    """

    next_bus_after_service_gap: str | None
    """
    If this prediction is the last arrival (for this route) before a service gap,
    this represents the number of minutes until the next scheduled bus arrival (from the prediction time).
    """

    scheduled_start_time_seconds: int
    """
    Contains the time (in seconds past midnight) of the scheduled start of the trip.
    """

    scheduled_start_date: str
    """
    Contains the date (in “yyyy-mm-dd” format) of the scheduled start of the trip.
    """

    flag_stop_code: int
    """
    An integer code representing the flag-stop information for the prediction.

    `-1` = `UNDEFINED`
        No flag-stop information available
    `0` = `NORMAL`
        Normal stop
    `1` = `PICKUP_AND_DISCHARGE`
        Flag stop for both pickup and discharge
    `2` = `ONLY_DISCHARGE`
        Flag stop for discharge only
    """

    def __post_init__(self: Prediction) -> None:
        self.timestamp = to_datetime(self.timestamp)
        self.predicted_time = to_datetime(self.predicted_time)
