from dataclasses import dataclass
from typing import Type, Optional, Dict


@dataclass
class Operation(object):
    id: str
    """Operation ID of this operation."""

    path: str
    """Path relative to the base URL at which the operation is accessed."""

    verb: str
    """HTTP verb used to invoke the operation."""

    request_body_type: Optional[Type]
    """Data type describing the contents of the request body, or None if no request body."""

    response_body_type: Dict[int, Optional[Type]]
    """Data type describing the contents of the response body provided with the corresponding status code."""
