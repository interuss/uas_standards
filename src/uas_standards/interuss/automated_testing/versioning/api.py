"""Data types and operations from Versioning Automated Testing Interface 0.1.2 OpenAPI"""

# This file is autogenerated; do not modify manually!

from __future__ import annotations

from enum import Enum
from typing import Dict, Optional

from uas_standards import Operation

from implicitdict import ImplicitDict


API_VERSION = "0.1.2"
"""Version of Versioning Automated Testing Interface OpenAPI specification from which the objects in this package were generated."""

SystemBoundaryIdentifier = str
"""Identifier of a system boundary, known to both the client and the USS separate from this API, for which this interface can provide a version.  While the format is not prescribed by this API, any value must be URL-safe.  It is recommended to use an approach similar to reverse-order Internet domain names and Java packages where the global scope is described with increasingly-precise identifiers joined by periods.  For instance, the system boundary containing the mandatory Network Identification U-space service might be identified with `gov.eu.uspace.v1.netid` because the authority defining this system boundary is a governmental organization (specifically, the European Union) with requirements imposed on the system under test by the U-space regulation (first version) -- specifically, the Network Identification Service section."""


VersionIdentifier = str
"""Identifier of a particular version of a system (defined by a known system boundary).  While the format is not prescribed by this API, a semantic version (https://semver.org/) prefixed with a `v` is recommended."""


class GetVersionResponse(ImplicitDict):
    system_identity: Optional[SystemBoundaryIdentifier]
    """The requested system identity/boundary."""

    system_version: Optional[VersionIdentifier]
    """The version of the system with the specified system identity/boundary."""


class OperationID(str, Enum):
    GetVersion = "GetVersion"


OPERATIONS: Dict[OperationID, Operation] = {
    OperationID.GetVersion: Operation(
        id="GetVersion",
        path="/versions/{system_identity}",
        verb="GET",
        request_body_type=None,
        response_body_type={
            200: GetVersionResponse,
            401: None,
            403: None,
            404: None,
        }
    ),
}
