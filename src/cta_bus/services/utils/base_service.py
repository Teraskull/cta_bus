from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cta_bus.client import Client
    from cta_bus.ctatypes import BustimeResponseType, SystemTimeResponseType

from cta_bus.exceptions import (
    InvalidKeyError,
    InvalidParamError,
    InvalidResponseError,
    MaxIdentifiersError,
    UnknownMessageError,  # noqa: F401
)
from cta_bus.models import ErrorObject


class BaseService(ABC):
    def __init__(self: BaseService, client: Client) -> None:
        super().__init__()
        self.client = client

    def _check_for_errors(self: BaseService, result: BustimeResponseType) -> list[dict[str, str]]:
        """Check the response data for errors and validate if the format is correct.

        If the error is of "No data" type, return a list of those errors.
        Examples of "No data" type errors: "No data found for parameter", "No service scheduled", "No arrival times"
        Otherwise raise an exception.
        """
        bustime_response = result.get("bustime-response")

        if not bustime_response:
            msg = "Response is not a valid Bustime response"
            raise InvalidResponseError(msg)

        error_obj = bustime_response.get("error")
        if error_obj:
            error_msg: str = error_obj[0]["msg"]  # Assume only one error for some cases.

            if error_msg in (
                "No API access key supplied",
                "Invalid API access key supplied",
                "No API access permitted"
            ):
                raise InvalidKeyError(error_msg)

            if error_msg == "No parameter provided":
                raise InvalidParamError(error_msg)

            if "identifiers exceeded" in error_msg:
                raise MaxIdentifiersError(error_msg)

            return [
                {
                    "message": error["msg"],
                    "error_data": {key: value for key, value in error.items() if key != "msg"}
                }
                for error in error_obj
            ]

            # raise UnknownMessageException(f"Unknown error message: '{error_msg}'")

        return []

    def build_error_objects(self: BaseService, data: BustimeResponseType | SystemTimeResponseType) -> list[ErrorObject]:
        """Build error objects if there are any errors from the API."""
        return [ErrorObject(**error) for error in self._check_for_errors(data)]

    @property
    @abstractmethod
    def path(self: BaseService) -> str:
        """The API endpoint with `/` prepended."""

    @abstractmethod
    def parse(self: BaseService, data: BustimeResponseType | SystemTimeResponseType) -> list:
        """Parse the response data and return a list of objects."""

    @abstractmethod
    def get_list(self: BaseService, params: dict) -> list:
        """Send the API request and return a list of objects."""
