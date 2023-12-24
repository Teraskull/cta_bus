from datetime import datetime

import pendulum
from pendulum.parsing.exceptions import ParserError

local_tz = pendulum.timezone("America/Chicago")


def to_datetime(timestamp: str) -> datetime:
    """Convert timestamp from UNIX or `YYYYMMDD HH:MM:SS` format to `datetime` object."""
    try:
        return pendulum.parse(timestamp, tz=local_tz)
    except ParserError:  # Assume that this is a UNIX timestamp in milliseconds.
        return pendulum.from_timestamp(float(timestamp) // 1000, tz=local_tz)
