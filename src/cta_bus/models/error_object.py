from dataclasses import dataclass


@dataclass
class ErrorObject:
    message: str
    """
    Error message.
    """

    error_data: dict
    """
    Key-value pairs of error data.
    """
