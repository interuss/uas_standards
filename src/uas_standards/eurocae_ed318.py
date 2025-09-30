from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from implicitdict import ImplicitDict, StringBasedDateTime


class CodeAuthorityRole(str, Enum):
    AUTHORIZATION = "AUTHORIZATION"
    NOTIFICATION = "NOTIFICATION"
    INFORMATION = "INFORMATION"


class CodeDaylightEventType(str, Enum):
    BMCT = "BMCT"
    SR = "SR"
    SS = "SS"
    EECT = "EECT"


class UomDistance(str, Enum):
    M = "m"
    FT = "ft"


CodeZoneIdentifierType = str

CodeCountryISOType = str


class CodeZoneVariantType(str, Enum):
    COMMON = "COMMON"
    CUSTOMIZED = "CUSTOMIZED"


class CodeZoneType(str, Enum):
    USPACE = "USPACE"
    PROHIBITED = "PROHIBITED"
    REQ_AUTHORIZATION = "REQ_AUTHORIZATION"
    CONDITIONAL = "CONDITIONAL"
    NO_RESTRICTION = "NO_RESTRICTION"


ConditionExpressionType = str


class CodeZoneReasonType(str, Enum):
    AIR_TRAFFIC = "AIR_TRAFFIC"
    SENSITIVE = "SENSITIVE"
    PRIVACY = "PRIVACY"
    POPULATION = "POPULATION"
    NATURE = "NATURE"
    NOISE = "NOISE"
    EMERGENCY = "EMERGENCY"
    DAR = "DAR"
    OTHER = "OTHER"


class TextShortType(ImplicitDict):
    # This complies with the JSON schema provided in the appendix E of the standard
    # Though, from the description, lang should be optional and text required.
    text: str | None
    lang: str


class TextLongType(ImplicitDict):
    # This complies with the JSON schema provided in the appendix E of the standard
    # Though, from the description, lang should be optional and text required.
    text: str | None
    lang: str


class CodeWeekDayType(str, Enum):
    MON = "MON"
    TUE = "TUE"
    WED = "WED"
    THU = "THU"
    FRI = "FRI"
    SAT = "SAT"
    SUN = "SUN"
    ANY = "ANY"


DateTimeType = StringBasedDateTime

TimeInterval = str  # TODO: Create appropriate type

TimeType = str  # TODO: Create appropriate type


class CodeYesNoType(str, Enum):
    YES = "YES"
    NO = "NO"


URNType = str


class VerticalLayer(ImplicitDict):
    upper: float
    upperReference: CodeVerticalReferenceType
    lower: float
    lowerReference: CodeVerticalReferenceType
    uom: UomDistance


class Layered(ImplicitDict):
    layer: VerticalLayer | None
    bbox: list[float] | None


class Point(Layered):
    type: Literal["Point"]
    coordinates: list[float]
    extent: ExtentCircle | None


class ExtentCircle(ImplicitDict):
    subType: Literal["Circle"]
    radius: float


class LineString(Layered):
    type: Literal["LineString"]
    coordinates: list[list[float]]


class Polygon(Layered):
    type: Literal["Polygon"]
    coordinates: list[list[list[float]]]


class MultiPoint(Layered):
    type: Literal["MultiPoint"]
    coordinates: list[list[float]]


class MultiLineString(Layered):
    type: Literal["MultiLineString"]
    coordinates: list[list[list[float]]]


class MultiPolygon(Layered):
    type: Literal["MultiPolygon"]
    coordinates: list[list[list[list[float]]]]


class GeometryCollection(ImplicitDict):
    type: Literal["GeometryCollection"]
    geometries: list[Any]


Geometry = (
    Point
    | LineString
    | Polygon
    | MultiPoint
    | MultiLineString
    | MultiPolygon
    | GeometryCollection
    | dict[str, Any]
)  # fallback for GeometryCollection or future types


class CodeVerticalReferenceType(str, Enum):
    AGL = "AGL"
    AMSL = "AMSL"
    WGS84 = "WGS84"


# Data models objects


class DatasetMetadata(ImplicitDict):
    provider: list[TextShortType] | None
    issued: DateTimeType | None
    validFrom: DateTimeType | None
    validTo: DateTimeType | None
    description: list[TextShortType] | None
    otherGeoid: URNType | None
    technicalLimitations: list[TextShortType] | None


class UASZone(ImplicitDict):
    identifier: CodeZoneIdentifierType
    country: CodeCountryISOType
    name: list[TextShortType] | None
    type: CodeZoneType
    variant: CodeZoneVariantType
    restrictionConditions: ConditionExpressionType | None
    region: int | None
    reason: list[CodeZoneReasonType] | None
    otherReasonInfo: list[TextShortType] | None
    regulationExemption: CodeYesNoType | None
    message: list[TextLongType] | None
    extendedProperties: dict[str, Any] | None
    limitedApplicability: list[TimePeriod] | None
    zoneAuthority: list[Authority]
    dataSource: Metadata | None


class TimePeriod(ImplicitDict):
    startDateTime: DateTimeType | None
    endDateTime: DateTimeType | None
    schedule: list[DailyPeriod] | None


class DailyPeriod(ImplicitDict):
    day: list[CodeWeekDayType]
    startTime: TimeType | None
    startEvent: CodeDaylightEventType | None
    endTime: TimeType | None
    endEvent: CodeDaylightEventType | None


class Authority(ImplicitDict):
    purpose: CodeAuthorityRole
    intervalBefore: TimeInterval | None
    name: list[TextShortType] | None
    service: list[TextShortType] | None
    contactName: list[TextShortType] | None
    siteURL: TextShortType | None
    email: TextShortType | None
    phone: TextShortType | None


class Metadata(ImplicitDict):
    creationDateTime: DateTimeType | None
    updateDateTime: DateTimeType | None
    originator: str | None


class Feature(ImplicitDict):
    type: Literal["Feature"]
    id: int | str | None
    properties: UASZone | None
    geometry: Geometry | None
    bbox: list[float] | None


class ED318Schema(ImplicitDict):
    """Top-level ED-318 FeatureCollection payload."""

    type: Literal["FeatureCollection"]
    name: str | None
    metadata: DatasetMetadata
    title: str | None
    bbox: list[float] | None
    features: list[Feature]

    @staticmethod
    def from_dict(obj: dict) -> ED318Schema:
        """Parse a raw dict into typed ED-318 classes using implicitdict."""
        return ImplicitDict.parse(obj, ED318Schema)
