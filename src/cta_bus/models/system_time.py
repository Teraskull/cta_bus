from dataclasses import dataclass
from datetime import datetime

from cta_bus.utils import to_datetime


@dataclass
class SystemTime:
    timestamp: datetime
    """
    The current system date and time (local).
    """

    def __post_init__(self: "SystemTime") -> None:
        self.timestamp = to_datetime(self.timestamp)
