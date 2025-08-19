from datetime import time
from enum import Enum
from typing import Any

import arrow
from implicitdict import ImplicitDict, StringBasedDateTime


class Restriction(str, Enum):
    PROHIBITED = "PROHIBITED"
    REQ_AUTHORISATION = "REQ_AUTHORISATION"
    CONDITIONAL = "CONDITIONAL"
    NO_RESTRICTION = "NO_RESTRICTION"


class Reason(str, Enum):
    AIR_TRAFFIC = "AIR_TRAFFIC"
    SENSITIVE = "SENSITIVE"
    PRIVACY = "PRIVACY"
    POPULATION = "POPULATION"
    NATURE = "NATURE"
    NOISE = "NOISE"
    FOREIGN_TERRITORY = "FOREIGN_TERRITORY"
    EMERGENCY = "EMERGENCY"
    OTHER = "OTHER"


class YESNO(str, Enum):
    YES = "YES"
    NO = "NO"


class Purpose(str, Enum):
    AUTHORIZATION = "AUTHORIZATION"
    NOTIFICATION = "NOTIFICATION"
    INFORMATION = "INFORMATION"


class UASZoneAuthority(ImplicitDict):
    name: str | None  # max length: 200
    service: str | None  # max length: 200
    email: str | None
    contactName: str | None  # max length: 200
    siteURL: str | None
    phone: str | None  # max length: 200
    purpose: Purpose | None
    intervalBefore: str | None


class VerticalReferenceType(str, Enum):
    AGL = "AGL"
    AMSL = "AMSL"


class HorizontalProjectionType(str, Enum):
    Circle = "Circle"
    Polygon = "Polygon"


class CircleOrPolygonType(ImplicitDict):
    type: HorizontalProjectionType
    center: list[float] | None  # 2 items. Coordinates: lat, lng
    radius: float | None  # > 0
    coordinates: (
        list[list[list[float]]] | None
    )  # List of polygons -> List of points: min 4 items -> Coordinates: lat, lng


class UomDimensions(str, Enum):
    M = "M"
    FT = "FT"


class UASZoneAirspaceVolume(ImplicitDict):
    uomDimensions: UomDimensions
    lowerLimit: int | None
    lowerVerticalReference: VerticalReferenceType
    upperLimit: int | None
    upperVerticalReference: VerticalReferenceType
    horizontalProjection: CircleOrPolygonType


class WeekDateType(str, Enum):
    MON = "MON"
    TUE = "TUE"
    WED = "WED"
    THU = "THU"
    FRI = "FRI"
    SAT = "SAT"
    SUN = "SUN"
    ANY = "ANY"


class ED269TimeType(str):
    """String that allows values which describe a time in ED-269 flavour of ISO 8601 format.

    ED-269 standard specifies that a time instant type should be in the form of hh:mmS where S is
    the timezone. However, examples are using the following format: 00:00:00.00Z
    This class supports both formats as inputs and uses the long form as the output format.
    """

    time: time
    """`time` representation of the str value with timezone"""

    def __new__(cls, value: str | time):
        if isinstance(value, str):
            t = arrow.get(value, ["HH:mm:ss.SZ", "HH:mmZ"]).timetz()
        else:
            t = value
        str_value = str.__new__(
            cls, t.strftime("%H:%M:%S.%f")[:11] + t.strftime("%z").replace("+0000", "Z")
        )
        str_value.time = t
        return str_value


class DailyPeriod(ImplicitDict):
    day: list[WeekDateType]  # min items: 1, max items: 7
    startTime: ED269TimeType
    endTime: ED269TimeType


class ApplicableTimePeriod(ImplicitDict):
    permanent: YESNO
    startDateTime: StringBasedDateTime | None
    endDateTime: StringBasedDateTime | None
    schedule: list[DailyPeriod] | None  # min items: 1


class UASZoneVersion(ImplicitDict):
    title: str | None
    identifier: str  # max length: 7
    country: str  # length: 3
    name: str | None  # max length: 200
    type: str
    restriction: Restriction
    restrictionConditions: list[str] | None
    region: int | None
    reason: list[Reason] | None  # max length: 9
    otherReasonInfo: str | None  # max length: 30
    regulationExemption: YESNO | None
    uSpaceClass: str | None  # max length: 100
    message: str | None  # max length: 200
    applicability: list[ApplicableTimePeriod]
    zoneAuthority: list[UASZoneAuthority]
    geometry: list[UASZoneAirspaceVolume]  # min items: 1
    extendedProperties: Any | None


class ED269Schema(ImplicitDict):
    title: str | None
    description: str | None
    features: list[UASZoneVersion]

    @staticmethod
    def from_dict(raw_data: dict) -> "ED269Schema":
        return ImplicitDict.parse(raw_data, ED269Schema)
