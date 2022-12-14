"""Data types from Geo-Awareness Automated Test Interfaces 0.1.0 OpenAPI"""

# This file is autogenerated; do not modify manually!

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from implicitdict import ImplicitDict, StringBasedDateTime


UUIDv4Format = str
"""String whose format matches a version-4 UUID according to RFC 4122."""


class StatusResponseStatus(str, Enum):
    """The status of the USS automated testing interface.
    - `Starting`: the USS is starting and the automated test driver should wait before sending requests.
    - `Ready`: the USS is ready to receive test requests.
    """

    Starting = "Starting"
    Ready = "Ready"


class StatusResponse(ImplicitDict):
    status: StatusResponseStatus
    """The status of the USS automated testing interface.
    - `Starting`: the USS is starting and the automated test driver should wait before sending requests.
    - `Ready`: the USS is ready to receive test requests.
    """

    version: Optional[str]
    """Arbitrary string representing the version of the USS system to be tested."""


class GeozoneHttpsSourceFormat(str, Enum):
    """The format of the response expected from the source."""

    ED_269 = "ED-269"


class GeozoneHttpsSource(ImplicitDict):
    url: str
    """The URL at which the Geozone data shall be downloaded from."""

    format: Optional[GeozoneHttpsSourceFormat] = GeozoneHttpsSourceFormat.ED_269
    """The format of the response expected from the source."""


class GeozoneSourceResponseResult(str, Enum):
    """The status of the Geozone source and the handling of its data by the USS.
    - `Activating`: the USS is processing the request and is currently activating the Geozone data.
    - `Ready`: the Geozone data has been successfully activated and the USS is ready to receive test requests.
    - `Deactivating`: the Geozone data is being deactivated.
    - `Unsupported`: the USS cannot process the dataset type specified.
    - `Rejected`: the Geozone data was rejected because it is invalid.
    - `Error`: the Geozone data activation or deactivation failed. The message field is required in this case.
    """

    Activating = "Activating"
    Ready = "Ready"
    Deactivating = "Deactivating"
    Unsupported = "Unsupported"
    Rejected = "Rejected"
    Error = "Error"


class GeozoneSourceResponse(ImplicitDict):
    result: GeozoneSourceResponseResult
    """The status of the Geozone source and the handling of its data by the USS.
    - `Activating`: the USS is processing the request and is currently activating the Geozone data.
    - `Ready`: the Geozone data has been successfully activated and the USS is ready to receive test requests.
    - `Deactivating`: the Geozone data is being deactivated.
    - `Unsupported`: the USS cannot process the dataset type specified.
    - `Rejected`: the Geozone data was rejected because it is invalid.
    - `Error`: the Geozone data activation or deactivation failed. The message field is required in this case.
    """

    message: Optional[str]
    """Human-readable explanation of the result for debugging purpose only. This field is required when the result value is `Error`."""


class UomDimensions(str, Enum):
    M = "M"
    FT = "FT"


class VerticalReferenceType(str, Enum):
    AGL = "AGL"
    AMSL = "AMSL"


USpaceClass = str


class Restriction(str, Enum):
    PROHIBITED = "PROHIBITED"
    REQ_AUTHORISATION = "REQ_AUTHORISATION"
    CONDITIONAL = "CONDITIONAL"
    NO_RESTRICTION = "NO_RESTRICTION"


class Position(ImplicitDict):
    uomDimensions: UomDimensions

    verticalReferenceType: VerticalReferenceType

    height: Optional[float] = 0
    """Height above vertical reference datum indicated in `verticalReferenceType`, in units of `uomDimensions`."""

    longitude: Optional[float] = 0
    """Longitude, degrees east of prime meridian."""

    latitude: Optional[float] = 0
    """Latitude, degrees north of the equator."""


class ED269Filters(ImplicitDict):
    """Filter criteria for the selection of Geozones according to ED-269 characteristics."""

    uSpaceClass: Optional[USpaceClass]
    """If specified, only select Geozones which are of the specified `uSpaceClass`."""

    acceptableRestrictions: Optional[List[Restriction]]
    """If specified and non-empty, only select Geozones which are one of the specified restriction types."""


class GeozonesCheckResultGeozone(str, Enum):
    """Indication of whether one or more applicable Geozones were selected according to the selection criteria of the corresponding check.
    * Present: One or more applicable Geozones were selected. * Absent: No applicable Geozones were selected. * UnsupportedFilter: Applicable Geozones could not be selected because one or more filter criteria are not supported by the USSP.  If this value is specified, `message` must be populated. * Error: An error or condition not enumerated above occurred.  If this value is specified, `message` must be populated.
    """

    Present = "Present"
    Absent = "Absent"
    UnsupportedFilter = "UnsupportedFilter"
    Error = "Error"


class GeozonesCheckResult(ImplicitDict):
    geozone: GeozonesCheckResultGeozone
    """Indication of whether one or more applicable Geozones were selected according to the selection criteria of the corresponding check.
    * Present: One or more applicable Geozones were selected. * Absent: No applicable Geozones were selected. * UnsupportedFilter: Applicable Geozones could not be selected because one or more filter criteria are not supported by the USSP.  If this value is specified, `message` must be populated. * Error: An error or condition not enumerated above occurred.  If this value is specified, `message` must be populated.
    """

    message: Optional[str]
    """A human-readable description of why the non-standard `geozone` value was reported.  Should only be populated when appropriate according to the value of the `geozone` field."""


class CreateGeozoneSourceRequest(ImplicitDict):
    https_source: Optional[GeozoneHttpsSource]


class GeozonesFilterSet(ImplicitDict):
    """Set of filters to select only a subset of Geozones.  Only Geozones which are applicable to all specified filters within this filter set should be selected."""

    position: Optional[Position]
    """If specified, only select Geozones encompassing this position."""

    after: Optional[StringBasedDateTime]
    """If specified, only select Geozones which encompass at least some times at or after this time."""

    before: Optional[StringBasedDateTime]
    """If specified, only select Geozones which encompass at least some times at or before this time."""

    ed269: Optional[ED269Filters]


class GeozonesCheckReply(ImplicitDict):
    applicableGeozone: Optional[List[GeozonesCheckResult]] = []
    """Responses to each of the `checks` in the request.  The number of entries in this array should match the number of entries in the `checks` field of the request."""


class GeozonesCheck(ImplicitDict):
    filterSets: List[GeozonesFilterSet]
    """Select Geozones which match any of the specified filter sets."""


class GeozonesCheckRequest(ImplicitDict):
    checks: List[GeozonesCheck]
