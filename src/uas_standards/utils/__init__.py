from dataclasses import dataclass


@dataclass
class Operation:
    id: str
    """Operation ID of this operation."""

    path: str
    """Path relative to the base URL at which the operation is accessed."""

    verb: str
    """HTTP verb used to invoke the operation."""

    request_body_type: type | None
    """Data type describing the contents of the request body, or None if no request body."""

    response_body_type: dict[int, type | None]
    """Data type describing the contents of the response body provided with the corresponding status code."""


__all__ = ["Operation"]
