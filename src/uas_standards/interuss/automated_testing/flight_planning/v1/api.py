"""Data types and operations from Flight Planning Automated Testing Interface 0.5.0 OpenAPI"""

# This file is autogenerated; do not modify manually!

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from uas_standards import Operation

from implicitdict import ImplicitDict, StringBasedDateTime


API_VERSION = "0.5.0"
"""Version of Flight Planning Automated Testing Interface OpenAPI specification from which the objects in this package were generated."""

FlightPlanID = str
"""String identifying a user flight plan.  Format matches a version-4 UUID according to RFC 4122."""


class StatusResponseStatus(str, Enum):
    """The status of this automated testing interface.
    - `Starting`: the interface is starting and the automated test driver should wait before sending requests.
    - `Ready`: the interface is ready to receive test requests.
    """

    Starting = "Starting"
    Ready = "Ready"


class StatusResponse(ImplicitDict):
    status: StatusResponseStatus
    """The status of this automated testing interface.
    - `Starting`: the interface is starting and the automated test driver should wait before sending requests.
    - `Ready`: the interface is ready to receive test requests.
    """

    api_name: Optional[str]
    """Indication of the API implemented at this URL.  Must be "Flight Planning Automated Testing Interface"."""

    api_version: Optional[str]
    """Indication of the API version implemented at this URL.  Must be "v0.5.0" when implementing this version of the API."""


class FlightPlanAdditionalInformation(ImplicitDict):
    """Any information relevant to a particular jurisdiction or use case not described in the standard schema. The keys and values must be agreed upon between the test designers and test participants."""



class BasicFlightPlanInformationUsageState(str, Enum):
    """User's current usage of the flight plan.
    `Planned`: The user intends to fly according to this flight plan, but is not currently using the defined
      area with an active UAS.

    `InUse`: The user is currently using the defined area with an active UAS.
    `Closed`: The user is no longer using, or planning to use, the flight plan.
    """

    Planned = "Planned"
    InUse = "InUse"
    Closed = "Closed"


class BasicFlightPlanInformationUasState(str, Enum):
    """State of the user's UAS associated with this flight plan.

      - `Nominal`: The user or UAS reports or implies that it is performing nominally, or has not indicated
        `OffNominal` or `Contingent`.

      - `OffNominal`: The user or UAS reports or implies that it is temporarily not conforming to its intent,
        but may expect to be able to recover to normal operation.

      - `Contingent`: The user or UAS reports or implies that it is not conforming to its intent and may be
        unable to recover to normal operation.

      - `NotSpecified`: The UAS status is not currently available or known (for instance, if the flight is
        planned in the future and the UAS that will be flying has not yet connected to the system).
    """

    Nominal = "Nominal"
    OffNominal = "OffNominal"
    Contingent = "Contingent"
    NotSpecified = "NotSpecified"


class ExecutionStyle(str, Enum):
    """The style of execution of a specified flight planning action that the operator would like the USS to perform.

      - `Hypothetical`: The user does not want the USS to actually perform any action regarding the actual flight plan.  Instead, the user would like to know the likely outcome if the action were hypothetically attempted.  The response to this request will not refer to an actual flight plan, or an actual state change in an existing flight plan, but rather a hypothetical flight plan or a hypothetical change to an existing flight plan.

      - `IfAllowed`: The user would like to perform the requested action if it is allowed.  If the requested action is allowed, the USS should actually perform the action (e.g., actually create a new ASTM F3548-21 operational intent).  If the requested action is not allowed, the USS should indicate that the action is Rejected and not perform the action.  The response to this request will refer to an actual flight plan when appropriate, and never refer to a hypothetical flight plan or status.

      - `InReality`: The user is communicating an actual state of reality.  The USS should consider the user to be actually performing (or attempting to perform) this action, regardless of whether or not the action is allowed under relevant UTM rules.
    """

    Hypothetical = "Hypothetical"
    IfAllowed = "IfAllowed"
    InReality = "InReality"


class PlanningActivityResult(str, Enum):
    """The result of a flight planning activity.

      - `Completed`: The user's flight plan has been updated according to the situation specified by the user. 

      - `Rejected`: The updates the user requested to their flight plan are not allowed according to the rules under which the flight plan is being managed.  The reasons for rejection may include a disallowed conflict with another flight during preflight.

      - `Failed`: The USS was not able to successfully authorize or update the flight plan due to a problem with the USS or a downstream system.

      - `NotSupported`: The USS's implementation does not support the attempted interaction.  For instance, if the request specified a high-priority flight and the USS does not support management of high-priority flights.
    """

    Completed = "Completed"
    Rejected = "Rejected"
    Failed = "Failed"
    NotSupported = "NotSupported"


class FlightPlanStatus(str, Enum):
    """The status of the user's flight plan.

      - `NotPlanned`: The USS has not created an authorized flight plan for the user.

      - `Planned`: The USS has created an authorized flight plan for the user, but the user may not yet start flying (even if within the time bounds of the flight plan).

      - `OkToFly`: The flight plan is in a state such that it is ok for the user to nominally fly within the bounds (including time) of the flight plan.

      - `OffNominal`: The flight plan now reflects the user's actions, but the flight plan is not in a nominal state (e.g., the USS has placed the ASTM F3548-21 operational intent into one of the Nonconforming or Contingent states).

      - `Closed`: The flight plan was closed successfully by the USS and is now out of the UTM system.
    """

    NotPlanned = "NotPlanned"
    Planned = "Planned"
    OkToFly = "OkToFly"
    OffNominal = "OffNominal"
    Closed = "Closed"


class AdvisoryInclusion(str, Enum):
    """Indication of whether any advisories or conditions were provided to the user along with the result of an associated flight planning attempt.

      - `Unknown`: It is unknown or irrelevant whether advisories or conditions were provided to the user

      - `AtLeastOneAdvisoryOrCondition`: At least one advisory or condition was provided to the user.

      - `NoAdvisoriesOrConditions`: No advisories or conditions were provided to the user.
    """

    Unknown = "Unknown"
    AtLeastOneAdvisoryOrCondition = "AtLeastOneAdvisoryOrCondition"
    NoAdvisoriesOrConditions = "NoAdvisoriesOrConditions"


class UpsertFlightPlanResponse(ImplicitDict):
    planning_result: PlanningActivityResult
    """The result of the flight plan creation or update attempt by the emulated user. If any option other than `Completed` is specified, the `notes` field should be populated with the reason for the unsuccessful outcome."""

    notes: Optional[str]
    """Human-readable explanation of the observed result.  This explanation may be made available to a human reviewing the test results, and ideally should explain why an undesirable result was obtained.  For instance, if the injection attempt Failed, then these notes may indicate that the attempt failed because the DSS indicated 400 to a valid request (perhaps also including the valid request as proof)."""

    flight_plan_status: FlightPlanStatus
    """The status of the user's flight plan following the flight planning activity."""

    includes_advisories: Optional[AdvisoryInclusion]
    """Nature of advisories included in the response to the user regarding their attempt to perform this flight planning activity."""


class DeleteFlightPlanResponse(ImplicitDict):
    planning_result: PlanningActivityResult
    """The result of attempted flight plan cancellation/closure by the USS admin. If any option other than `Completed` is specified, the `notes` field should be populated with the reason for the unsuccessful outcome."""

    notes: Optional[str]
    """Human-readable explanation of the observed result."""

    flight_plan_status: FlightPlanStatus
    """The status of the user's flight plan following the flight planning activity."""

    includes_advisories: Optional[AdvisoryInclusion]
    """Nature of advisories included in the response to the user regarding their attempt to cancel/close their flight plan."""


class ClearAreaOutcomeDetails(ImplicitDict):
    """Optional free-form structured data to augment `message`."""



class ClearAreaOutcome(ImplicitDict):
    success: Optional[bool] = False
    """True if, and only if, all flight plans in the specified area managed by the USS were canceled and removed."""

    message: Optional[str]
    """If the USS admin was unable to clear the entire area, this message can provide information on the problem encountered."""

    details: Optional[ClearAreaOutcomeDetails]
    """Optional free-form structured data to augment `message`."""


class ClearAreaResponse(ImplicitDict):
    outcome: ClearAreaOutcome


Priority = int
"""Ordinal priority of the operational intent, as defined in ASTM F3548-21."""


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


class RPAS26FlightDetailsOperatorType(str, Enum):
    """The type of operator."""

    Recreational = "Recreational"
    CommercialExcluded = "CommercialExcluded"
    ReOC = "ReOC"


class RPAS26FlightDetailsAircraftType(str, Enum):
    """Type of vehicle being used as per ASTM F3411-22a."""

    NotDeclared = "NotDeclared"
    Aeroplane = "Aeroplane"
    Helicopter = "Helicopter"
    Gyroplane = "Gyroplane"
    HybridLift = "HybridLift"
    Ornithopter = "Ornithopter"
    Glider = "Glider"
    Kite = "Kite"
    FreeBalloon = "FreeBalloon"
    CaptiveBalloon = "CaptiveBalloon"
    Airship = "Airship"
    FreeFallOrParachute = "FreeFallOrParachute"
    Rocket = "Rocket"
    TetheredPoweredAircraft = "TetheredPoweredAircraft"
    GroundObstacle = "GroundObstacle"
    Other = "Other"


class RPAS26FlightDetailsFlightProfile(str, Enum):
    """Type of flight profile."""

    AutomatedGrid = "AutomatedGrid"
    AutomatedWaypoint = "AutomatedWaypoint"
    Manual = "Manual"


class RPAS26FlightDetails(ImplicitDict):
    """Information about a flight necessary to plan successfully using the RPAS Platform Operating Rules version 2.6."""

    operator_type: Optional[RPAS26FlightDetailsOperatorType]
    """The type of operator."""

    uas_serial_numbers: Optional[List[str]]
    """The list of UAS/drone serial numbers that will be operated during the operation."""

    uas_registration_numbers: Optional[List[str]]
    """The list of UAS/drone registration numbers that will be operated during the operation."""

    aircraft_type: Optional[RPAS26FlightDetailsAircraftType]
    """Type of vehicle being used as per ASTM F3411-22a."""

    flight_profile: Optional[RPAS26FlightDetailsFlightProfile]
    """Type of flight profile."""

    pilot_license_number: Optional[str]
    """License number for the pilot."""

    pilot_phone_number: Optional[str]
    """Contact phone number for the pilot."""

    operator_number: Optional[str]
    """Operator number."""


Longitude = float
"""Degrees of longitude east of the Prime Meridian, with reference to the WGS84 ellipsoid."""


Latitude = float
"""Degrees of latitude north of the equator, with reference to the WGS84 ellipsoid."""


class RadiusUnits(str, Enum):
    """FIXM-compatible units.  Only meters ("M") are acceptable for UTM."""

    M = "M"


class Radius(ImplicitDict):
    value: float
    """Distance from the centerpoint of a circular area, along the WGS84 ellipsoid."""

    units: RadiusUnits = RadiusUnits.M
    """FIXM-compatible units.  Only meters ("M") are acceptable for UTM."""


class AltitudeReference(str, Enum):
    """A code indicating the reference for a vertical distance. See AIXM 5.1 and FIXM 4.2.0."""

    W84 = "W84"
    SFC = "SFC"


class AltitudeUnits(str, Enum):
    """The reference quantities used to express the value of altitude. See FIXM 4.2. Currently, UTM only allows meters with no immediate plans to allow other options."""

    M = "M"


class Altitude(ImplicitDict):
    value: float
    """The numeric value of the altitude. Note that min and max values are added as a sanity check. As use cases evolve and more options are made available in terms of units of measure or reference systems, these bounds may be re-evaluated."""

    reference: AltitudeReference
    """A code indicating the reference for a vertical distance. See AIXM 5.1 and FIXM 4.2.0."""

    units: AltitudeUnits = AltitudeUnits.M
    """The reference quantities used to express the value of altitude. See FIXM 4.2. Currently, UTM only allows meters with no immediate plans to allow other options."""


class TimeFormat(str, Enum):
    RFC3339 = "RFC3339"


class Time(ImplicitDict):
    value: StringBasedDateTime
    """RFC3339-formatted time/date string.  The time zone must be 'Z'."""

    format: TimeFormat = TimeFormat.RFC3339


UserNotificationConflicts = str
"""Conflict status as indicated in the notification.            
 - `Unknown`: Notification doesn't contain information regarding conflicts.
 - `None`: Notification indicates no conflicts.
 - `Single`: Notification indicates the presence of one conflict.
 - `Multiple`: Notification indicates the presence of multiple conflicts.

Acceptable values:
* Unknown
* None
* Single
* Multiple
"""


class UserNotification(ImplicitDict):
    """Notification observed by virtual user."""

    observed_at: Time
    """Time at which the virtual user observed the notification."""

    conflicts: Optional[UserNotificationConflicts] = "Unknown"
    """Conflict status as indicated in the notification.            
     - `Unknown`: Notification doesn't contain information regarding conflicts.
     - `None`: Notification indicates no conflicts.
     - `Single`: Notification indicates the presence of one conflict.
     - `Multiple`: Notification indicates the presence of multiple conflicts.
    """


class QueryUserNotificationsResponse(ImplicitDict):
    """Response object for query request for notifications observed by the virtual user."""

    user_notifications: List[UserNotification]
    """List of applicable observed user notifications."""


class ASTMF354821OpIntentInformation(ImplicitDict):
    """Information provided about a flight plan that is necessary for ASTM F3548-21."""

    priority: Optional[Priority]


class FlightAuthorisationData(ImplicitDict):
    """The details of a UAS flight authorization request, as received from the user.

    Note that a full description of a flight authorisation must include mandatory information required by ANNEX IV of COMMISSION IMPLEMENTING REGULATION (EU) 2021/664 for an UAS flight authorisation request. Reference: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32021R0664&from=EN#d1e32-178-1
    """

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


class LatLngPoint(ImplicitDict):
    """Point on the earth's surface."""

    lng: Longitude

    lat: Latitude


class Polygon(ImplicitDict):
    """An enclosed area on the earth. The bounding edges of this polygon are defined to be the shortest paths between connected vertices.  This means, for instance, that the edge between two points both defined at a particular latitude is not generally contained at that latitude. The winding order must be interpreted as the order which produces the smaller area. The path between two vertices is defined to be the shortest possible path between those vertices. Edges may not cross. Vertices may not be duplicated.  In particular, the final polygon vertex must not be identical to the first vertex."""

    vertices: List[LatLngPoint]


class Circle(ImplicitDict):
    """A circular area on the surface of the earth."""

    center: Optional[LatLngPoint]

    radius: Optional[Radius]


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


class BasicFlightPlanInformation(ImplicitDict):
    """Basic information about a flight plan that a user and/or UAS can be expected to provide in most flight planning scenarios."""

    usage_state: BasicFlightPlanInformationUsageState
    """User's current usage of the flight plan.
    `Planned`: The user intends to fly according to this flight plan, but is not currently using the defined
      area with an active UAS.

    `InUse`: The user is currently using the defined area with an active UAS.
    `Closed`: The user is no longer using, or planning to use, the flight plan.
    """

    uas_state: BasicFlightPlanInformationUasState
    """State of the user's UAS associated with this flight plan.

      - `Nominal`: The user or UAS reports or implies that it is performing nominally, or has not indicated
        `OffNominal` or `Contingent`.

      - `OffNominal`: The user or UAS reports or implies that it is temporarily not conforming to its intent,
        but may expect to be able to recover to normal operation.

      - `Contingent`: The user or UAS reports or implies that it is not conforming to its intent and may be
        unable to recover to normal operation.

      - `NotSpecified`: The UAS status is not currently available or known (for instance, if the flight is
        planned in the future and the UAS that will be flying has not yet connected to the system).
    """

    area: Optional[List[Volume4D]] = []
    """The complete area in which the user intends to fly, or may fly, as known by the user.  The user intends to fly, or may fly, anywhere in this entire area.
    This means, for instance, that an ASTM F3548-21 operational intent supporting this flight must have volumes that are a superset of this area.  If the operational intent did not cover this entire area, then all of the intended flight would not be covered by the operational intent (for at least part of the flight, the operator intends to fly outside the operational intent).
    """


class ClearAreaRequest(ImplicitDict):
    request_id: str
    """Unique string identifying this request.  If a second request with an identical ID is received, the USS may return the same response from the previous operation rather than attempting to clear the area again (the USS may also attempt to clear the area again)."""

    extent: Volume4D
    """The USS admin should cancel and remove any flight plan it manages where any part of that flight plan intersects this area."""


class FlightPlan(ImplicitDict):
    """Details of user's intent to create or modify a flight plan."""

    basic_information: BasicFlightPlanInformation

    astm_f3548_21: Optional[ASTMF354821OpIntentInformation]

    uspace_flight_authorisation: Optional[FlightAuthorisationData]

    rpas_operating_rules_2_6: Optional[RPAS26FlightDetails]

    additional_information: Optional[FlightPlanAdditionalInformation]
    """Any information relevant to a particular jurisdiction or use case not described in the standard schema. The keys and values must be agreed upon between the test designers and test participants."""


class UpsertFlightPlanRequest(ImplicitDict):
    """Client request to emulate a user performing a flight planning action."""

    flight_plan: FlightPlan
    """Complete new or updated information about the flight describing the flight planning action to be taken."""

    execution_style: ExecutionStyle
    """Style of execution for the requested flight planning action."""

    request_id: str
    """ID uniquely identifying the upsertion request.  If additional requests are received with the same request_id, the response from the first request should be returned, or an error indicated."""


class OperationID(str, Enum):
    GetStatus = "GetStatus"
    ClearArea = "ClearArea"
    UpsertFlightPlan = "UpsertFlightPlan"
    DeleteFlightPlan = "DeleteFlightPlan"
    QueryUserNotifications = "QueryUserNotifications"


OPERATIONS: Dict[OperationID, Operation] = {
    OperationID.GetStatus: Operation(
        id="GetStatus",
        path="/status",
        verb="GET",
        request_body_type=None,
        response_body_type={
            200: StatusResponse,
            401: None,
            403: None,
            404: None,
        }
    ),
    OperationID.ClearArea: Operation(
        id="ClearArea",
        path="/clear_area_requests",
        verb="POST",
        request_body_type=ClearAreaRequest,
        response_body_type={
            200: ClearAreaResponse,
            401: None,
            403: None,
        }
    ),
    OperationID.UpsertFlightPlan: Operation(
        id="UpsertFlightPlan",
        path="/flight_plans/{flight_plan_id}",
        verb="PUT",
        request_body_type=UpsertFlightPlanRequest,
        response_body_type={
            200: UpsertFlightPlanResponse,
            401: None,
            403: None,
            409: None,
        }
    ),
    OperationID.DeleteFlightPlan: Operation(
        id="DeleteFlightPlan",
        path="/flight_plans/{flight_plan_id}",
        verb="DELETE",
        request_body_type=None,
        response_body_type={
            200: DeleteFlightPlanResponse,
            401: None,
            403: None,
            404: None,
        }
    ),
    OperationID.QueryUserNotifications: Operation(
        id="QueryUserNotifications",
        path="/user_notifications",
        verb="GET",
        request_body_type=None,
        response_body_type={
            200: QueryUserNotificationsResponse,
            400: None,
            401: None,
            403: None,
        }
    ),
}
