"""Data types and operations from Strategic Coordination Test Data Injection 0.2.2 OpenAPI"""

# This file is autogenerated; do not modify manually!

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from uas_standards import Operation

from implicitdict import ImplicitDict, StringBasedDateTime


API_VERSION = "0.2.2"
"""Version of Strategic Coordination Test Data Injection OpenAPI specification from which the objects in this package were generated."""

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


UUIDv4Format = str
"""String whose format matches a version-4 UUID according to RFC 4122."""


EntityID = UUIDv4Format


class TimeFormat(str, Enum):
    RFC3339 = "RFC3339"


class Time(ImplicitDict):
    value: StringBasedDateTime
    """RFC3339-formatted time/date string.  The time zone must be 'Z'."""

    format: TimeFormat = TimeFormat.RFC3339


class RadiusUnits(str, Enum):
    """FIXM-compatible units.  Only meters ("M") are acceptable for UTM."""

    M = "M"


class Radius(ImplicitDict):
    value: float
    """Distance from the centerpoint of a circular area, along the WGS84 ellipsoid."""

    units: RadiusUnits = RadiusUnits.M
    """FIXM-compatible units.  Only meters ("M") are acceptable for UTM."""


class AltitudeReference(str, Enum):
    """A code indicating the reference for a vertical distance. See AIXM 5.1 and FIXM 4.2.0. Currently, UTM only allows WGS84 with no immediate plans to allow other options. FIXM and AIXM allow for 'SFC' which is equivalent to AGL."""

    W84 = "W84"


class AltitudeUnits(str, Enum):
    """The reference quantities used to express the value of altitude. See FIXM 4.2. Currently, UTM only allows meters with no immediate plans to allow other options."""

    M = "M"


class Altitude(ImplicitDict):
    value: float
    """The numeric value of the altitude. Note that min and max values are added as a sanity check. As use cases evolve and more options are made available in terms of units of measure or reference systems, these bounds may be re-evaluated."""

    reference: AltitudeReference = AltitudeReference.W84
    """A code indicating the reference for a vertical distance. See AIXM 5.1 and FIXM 4.2.0. Currently, UTM only allows WGS84 with no immediate plans to allow other options. FIXM and AIXM allow for 'SFC' which is equivalent to AGL."""

    units: AltitudeUnits = AltitudeUnits.M
    """The reference quantities used to express the value of altitude. See FIXM 4.2. Currently, UTM only allows meters with no immediate plans to allow other options."""


Latitude = float
"""Degrees of latitude north of the equator, with reference to the WGS84 ellipsoid."""


Longitude = float
"""Degrees of longitude east of the Prime Meridian, with reference to the WGS84 ellipsoid."""


class LatLngPoint(ImplicitDict):
    """Point on the earth's surface."""

    lng: Longitude

    lat: Latitude


class Circle(ImplicitDict):
    """A circular area on the surface of the earth."""

    center: Optional[LatLngPoint]

    radius: Optional[Radius]


class OperationalIntentState(str, Enum):
    """State of an operational intent. 'Accepted': Operational intent is created and shared, but not yet in use; see standard text for more details. The create or update request for this operational intent reference must include a Key containing all OVNs for all relevant Entities. 'Activated': Operational intent is in active use; see standard text for more details. The create or update request for this operational intent reference must include a Key containing all OVNs for all relevant Entities. 'Nonconforming': UA is temporarily outside its volumes, but the situation is expected to be recoverable; see standard text for more details. In this state, the `/uss/v1/operational_intents/{entityid}/telemetry` USS-USS endpoint should respond, if available, to queries from USS peers.  The create or update request for this operational intent may omit a Key in this case because the operational intent is being adjusted as flown and cannot necessarily deconflict. 'Contingent': UA is considered unrecoverably unable to conform with its coordinate operational intent; see standard text for more details. This state must transition to Ended.  In this state, the `/uss/v1/operational_intents/{entityid}/telemetry` USS-USS endpoint should respond, if available, to queries from USS peers.  The create or update request for this operational intent may omit a Key in this case because the operational intent is being adjusted as flown and cannot necessarily deconflict."""

    Accepted = "Accepted"
    Activated = "Activated"
    Nonconforming = "Nonconforming"
    Contingent = "Contingent"


Priority = int
"""Ordinal priority of the operational intent, as defined by the regulator.  Operational intents with lesser values are lower priority than all operational intents with greater values.  A lower-priority operational intent may not create a conflict with a higher-priority operational intent.  A higher-priority operational intent may create a conflict with a lower-priority operational intent.  The regulator specifies whether an operational intent may create a conflict with other operational intents of the same priority."""


class FlightAuthorisationDataOperationCategory(str, Enum):
    """Category of UAS operation (‘open’, ‘specific’, ‘certified’) as defined in COMMISSION DELEGATED REGULATION (EU) 2019/945. Required by ANNEX IV of COMMISSION IMPLEMENTING REGULATION (EU) 2021/664, paragraph 4."""

    Unknown = "Unknown"
    Open = "Open"
    Specific = "Specific"
    Certified = "Certified"


class OperationMode(str, Enum):
    """Specify if the operation is a `VLOS` or `BVLOS` operation. Required by ANNEX IV of COMMISSION IMPLEMENTING REGULATION (EU) 2021/664, paragraph 2."""

    Undeclared = "Undeclared"
    Vlos = "Vlos"
    Bvlos = "Bvlos"


class UASClass(str, Enum):
    """Specify the class of the UAS to be flown, the specifition matches EASA class identification label categories. UAS aircraft class as defined in COMMISSION DELEGATED REGULATION (EU) 2019/945 (C0 to C4) and COMMISSION DELEGATED REGULATION (EU) 2020/1058 (C5 and C6). This field is required by ANNEX IV of COMMISSION IMPLEMENTING REGULATION (EU) 2021/664, paragraph 4."""

    Other = "Other"
    C0 = "C0"
    C1 = "C1"
    C2 = "C2"
    C3 = "C3"
    C4 = "C4"
    C5 = "C5"
    C6 = "C6"


class InjectFlightResponseResult(str, Enum):
    """The result of the flight submission. If any option other than `Planned` or `ReadyToFly` is specified, the `notes` field should be populated with the reason for the unsuccessful outcome.

      - `Planned`: The flight submission data was valid and the flight was successfully processed by the USS and is now authorized.

      - `ReadyToFly`: The flight is ready for the operator to begin flying.

      - `Rejected`: The flight submission data provided was invalid and/or could not be used to attempt to authorize the flight.  The reason for rejection may include a disallowed conflict with another flight.

      - `ConflictWithFlight`: (deprecated; use Rejected instead) The flight submission data was valid, but the flight could not be authorized because of a disallowed conflict with another flight.

      - `Failed`: The USS was not able to successfully authorize the flight due to a problem with the USS or a downstream system

      - `NotSupported`: The USS does not support the attempted interaction.  For instance, if the request specified a high-priority flight and the USS does not support management of high-priority flights.
    """

    Planned = "Planned"
    ReadyToFly = "ReadyToFly"
    Rejected = "Rejected"
    ConflictWithFlight = "ConflictWithFlight"
    Failed = "Failed"
    NotSupported = "NotSupported"


class InjectFlightResponse(ImplicitDict):
    result: InjectFlightResponseResult
    """The result of the flight submission. If any option other than `Planned` or `ReadyToFly` is specified, the `notes` field should be populated with the reason for the unsuccessful outcome.

      - `Planned`: The flight submission data was valid and the flight was successfully processed by the USS and is now authorized.

      - `ReadyToFly`: The flight is ready for the operator to begin flying.

      - `Rejected`: The flight submission data provided was invalid and/or could not be used to attempt to authorize the flight.  The reason for rejection may include a disallowed conflict with another flight.

      - `ConflictWithFlight`: (deprecated; use Rejected instead) The flight submission data was valid, but the flight could not be authorized because of a disallowed conflict with another flight.

      - `Failed`: The USS was not able to successfully authorize the flight due to a problem with the USS or a downstream system

      - `NotSupported`: The USS does not support the attempted interaction.  For instance, if the request specified a high-priority flight and the USS does not support management of high-priority flights.
    """

    notes: Optional[str]
    """Human-readable explanation of the observed result.  This explanation should be available to a human reviewing the test results, and ideally should explain why an undesirable result was obtained.  For instance, if the injection attempt Failed, then these notes may indicate that the attempt failed because the DSS indicated 400 to a valid request (perhaps also including the valid request as proof)."""

    operational_intent_id: Optional[EntityID]
    """The id of the operational intent communicated to the DSS. This value is only required when the result of the flight submission is `Planned`."""


class DeleteFlightResponseResult(str, Enum):
    """The result of attempted flight cancellation/closure

      - `Closed`: The flight was closed successfully by the USS and is now out of the UTM system.

      - `Failed`: The flight could not be closed successfully by the USS.
    """

    Closed = "Closed"
    Failed = "Failed"


class DeleteFlightResponse(ImplicitDict):
    result: DeleteFlightResponseResult
    """The result of attempted flight cancellation/closure

      - `Closed`: The flight was closed successfully by the USS and is now out of the UTM system.

      - `Failed`: The flight could not be closed successfully by the USS.
    """

    notes: Optional[str]
    """Human-readable explanation of the observed result."""


class ClearAreaOutcome(ImplicitDict):
    success: Optional[bool] = False
    """True if, and only if, all flights in the specified area owned by the USS were canceled and removed."""

    message: Optional[str]
    """If the USS was unable to clear the entire area, this message can provide information on the problem encountered."""

    timestamp: str
    """The time at which this operation was performed by the USS."""


class ClearAreaResponse(ImplicitDict):
    outcome: ClearAreaOutcome


class Capability(str, Enum):
    """Capability of a USS.

      `FlightAuthorisationValidation`: USS supports EU flight authorisation
        parameter validation.

      `BasicStrategicConflictDetection`: USS supports strategic conflict
        detection for typical flights, including future planning (Accepted
        operational intents), activation (Accepted operational intents), and
        closing (deleting the operational intent reference).

      `HighPriorityFlights`: USS supports flights at priority levels higher
        than typical flights.
    """

    FlightAuthorisationValidation = "FlightAuthorisationValidation"
    BasicStrategicConflictDetection = "BasicStrategicConflictDetection"
    HighPriorityFlights = "HighPriorityFlights"


class CapabilitiesResponse(ImplicitDict):
    capabilities: Optional[List[Capability]] = []
    """Set of capabilities supported by this USS."""


class Polygon(ImplicitDict):
    """An enclosed area on the earth. The bounding edges of this polygon are defined to be the shortest paths between connected vertices.  This means, for instance, that the edge between two points both defined at a particular latitude is not generally contained at that latitude. The winding order must be interpreted as the order which produces the smaller area. The path between two vertices is defined to be the shortest possible path between those vertices. Edges may not cross. Vertices may not be duplicated.  In particular, the final polygon vertex must not be identical to the first vertex."""

    vertices: List[LatLngPoint]


class Volume3D(ImplicitDict):
    """A three-dimensional geographic volume consisting of a vertically-extruded shape. Exactly one outline must be specified."""

    outline_circle: Optional[Circle]
    """A circular geographic shape on the surface of the earth."""

    outline_polygon: Optional[Polygon]
    """A polygonal geographic shape on the surface of the earth."""

    altitude_lower: Optional[Altitude]
    """Minimum bounding altitude of this volume. Must be less than altitude_upper, if specified."""

    altitude_upper: Optional[Altitude]
    """Maximum bounding altitude of this volume. Must be greater than altitude_lower, if specified."""


class Volume4D(ImplicitDict):
    """Contiguous block of geographic spacetime."""

    volume: Volume3D

    time_start: Optional[Time]
    """Beginning time of this volume. Must be before time_end."""

    time_end: Optional[Time]
    """End time of this volume. Must be after time_start."""


class OperationalIntentTestInjection(ImplicitDict):
    """Parameters that define an operational intent: this injection is used to create a operational intent reference in the DSS and also responding to requests for details of that operational intent (by other USSes or the test driver). The USS under test will need to process this data to both create a valid operational intent reference and responding to a query for details."""

    state: OperationalIntentState

    priority: Priority

    volumes: List[Volume4D]
    """Nominal volumes, as would be reported by a USS's operational_intents endpoint."""

    off_nominal_volumes: List[Volume4D]
    """Off-Nominal volumes, as would be reported by a USS's operational_intents endpoint."""


class FlightAuthorisationData(ImplicitDict):
    """A dataset to hold details of a UAS flight authorization request. Full description of a flight authorisation including mandatory information required by ANNEX IV of COMMISSION IMPLEMENTING REGULATION (EU) 2021/664 for an UAS flight authorisation request. Reference: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32021R0664&from=EN#d1e32-178-1"""

    uas_serial_number: str
    """Unique serial number of the unmanned aircraft or, if the unmanned aircraft is privately built, the unique serial number of the add-on. This is expressed in the ANSI/CTA-2063 Physical Serial Number format. Required by ANNEX IV of COMMISSION IMPLEMENTING REGULATION (EU) 2021/664, paragraph 1."""

    operation_mode: OperationMode

    operation_category: FlightAuthorisationDataOperationCategory
    """Category of UAS operation (‘open’, ‘specific’, ‘certified’) as defined in COMMISSION DELEGATED REGULATION (EU) 2019/945. Required by ANNEX IV of COMMISSION IMPLEMENTING REGULATION (EU) 2021/664, paragraph 4."""

    uas_class: UASClass

    identification_technologies: List[str]
    """Technology used to identify the UAS. Required by ANNEX IV of COMMISSION IMPLEMENTING REGULATION (EU) 2021/664, paragraph 6."""

    uas_type_certificate: Optional[str]
    """Provisional field. Not applicable as of September 2021. Required only if `uas_class` is set to `other` by ANNEX IV of COMMISSION IMPLEMENTING REGULATION (EU) 2021/664, paragraph 4."""

    connectivity_methods: List[str]
    """Connectivity methods. Required by ANNEX IV of COMMISSION IMPLEMENTING REGULATION (EU) 2021/664, paragraph 7."""

    endurance_minutes: int
    """Endurance of the UAS. This is expressed in minutes. Required by ANNEX IV of COMMISSION IMPLEMENTING REGULATION (EU) 2021/664, paragraph 8."""

    emergency_procedure_url: str
    """The URL at which the applicable emergency procedure in case of a loss of command and control link may be retrieved. Required by ANNEX IV of COMMISSION IMPLEMENTING REGULATION (EU) 2021/664, paragraph 9."""

    operator_id: str
    """Registration number of the UAS operator.
    The format is defined in EASA Easy Access Rules for Unmanned Aircraft Systems GM1 to AMC1
    Article 14(6) Registration of UAS operators and ‘certified’ UAS.
    Required by ANNEX IV of COMMISSION IMPLEMENTING REGULATION (EU) 2021/664, paragraph 10.
    """

    uas_id: Optional[str]
    """When applicable, the registration number of the unmanned aircraft.
    This is expressed using the nationality and registration mark of the unmanned aircraft in
    line with ICAO Annex 7.
    Specified by ANNEX IV of COMMISSION IMPLEMENTING REGULATION (EU) 2021/664, paragraph 10.
    """


class InjectFlightRequest(ImplicitDict):
    operational_intent: Optional[OperationalIntentTestInjection]

    flight_authorisation: Optional[FlightAuthorisationData]


class ClearAreaRequest(ImplicitDict):
    request_id: str
    """Unique string identifying this request.  If a second request with an identical ID is received, the USS may return the same response from the previous operation rather than attempting to clear the area again (the USS may also attempt to clear the area again)."""

    extent: Volume4D
    """The USS should cancel and remove any flight where any part of that flight intersects this area."""


class OperationID(str, Enum):
    GetStatus = "getStatus"
    GetCapabilities = "getCapabilities"
    InjectFlight = "injectFlight"
    DeleteFlight = "deleteFlight"
    ClearArea = "clearArea"


OPERATIONS: Dict[OperationID, Operation] = {
    OperationID.GetStatus: Operation(
        id="getStatus",
        path="/v1/status",
        verb="GET",
        request_body_type=None,
        response_body_type={
            200: StatusResponse,
            401: None,
            403: None,
            404: None,
        }
    ),
    OperationID.GetCapabilities: Operation(
        id="getCapabilities",
        path="/v1/capabilities",
        verb="GET",
        request_body_type=None,
        response_body_type={
            200: CapabilitiesResponse,
            401: None,
            403: None,
        }
    ),
    OperationID.InjectFlight: Operation(
        id="injectFlight",
        path="/v1/flights/{flight_id}",
        verb="PUT",
        request_body_type=InjectFlightRequest,
        response_body_type={
            200: InjectFlightResponse,
            401: None,
            403: None,
        }
    ),
    OperationID.DeleteFlight: Operation(
        id="deleteFlight",
        path="/v1/flights/{flight_id}",
        verb="DELETE",
        request_body_type=None,
        response_body_type={
            200: DeleteFlightResponse,
            401: None,
            403: None,
        }
    ),
    OperationID.ClearArea: Operation(
        id="clearArea",
        path="/v1/clear_area_requests",
        verb="POST",
        request_body_type=ClearAreaRequest,
        response_body_type={
            200: ClearAreaResponse,
            401: None,
            403: None,
        }
    ),
}
