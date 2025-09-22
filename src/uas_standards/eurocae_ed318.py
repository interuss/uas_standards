from __future__ import annotations
from enum import Enum
from typing import List, Optional, Union, Literal, Dict, Any
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
    text: Optional[str]
    lang: str


class TextLongType(ImplicitDict):
    # This complies with the JSON schema provided in the appendix E of the standard
    # Though, from the description, lang should be optional and text required.
    text: Optional[str]
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
    layer: Optional[VerticalLayer]
    bbox: Optional[List[float]]


class Point(Layered):
    type: Literal["Point"]
    coordinates: List[float]
    extent: Optional[ExtentCircle]


class ExtentCircle(ImplicitDict):
    subType: Literal["Circle"]
    radius: float


class LineString(Layered):
    type: Literal["LineString"]
    coordinates: List[List[float]]


class Polygon(Layered):
    type: Literal["Polygon"]
    coordinates: List[List[List[float]]]


class MultiPoint(Layered):
    type: Literal["MultiPoint"]
    coordinates: List[List[float]]


class MultiLineString(Layered):
    type: Literal["MultiLineString"]
    coordinates: List[List[List[float]]]


class MultiPolygon(Layered):
    type: Literal["MultiPolygon"]
    coordinates: List[List[List[List[float]]]]


class GeometryCollection(ImplicitDict):
    type: Literal["GeometryCollection"]
    geometries: List[Any]


Geometry = Union[
    Point,
    LineString,
    Polygon,
    MultiPoint,
    MultiLineString,
    MultiPolygon,
    GeometryCollection,
    Dict[str, Any],  # fallback for GeometryCollection or future types
]


class CodeVerticalReferenceType(str, Enum):
    AGL = "AGL"
    AMSL = "AMSL"
    WGS84 = "WGS84"


# Data models objects


class DatasetMetadata(ImplicitDict):
    provider: Optional[List[TextShortType]]
    issued: Optional[DateTimeType]
    validFrom: Optional[DateTimeType]
    validTo: Optional[DateTimeType]
    description: Optional[List[TextShortType]]
    otherGeoid: Optional[URNType]
    technicalLimitations: Optional[List[TextShortType]]


class UASZone(ImplicitDict):
    identifier: CodeZoneIdentifierType
    country: CodeCountryISOType
    name: Optional[List[TextShortType]]
    type: CodeZoneType
    variant: CodeZoneVariantType
    restrictionConditions: Optional[ConditionExpressionType]
    region: Optional[int]
    reason: Optional[List[CodeZoneReasonType]]
    otherReasonInfo: Optional[List[TextShortType]]
    regulationExemption: Optional[CodeYesNoType]
    message: Optional[List[TextLongType]]
    extendedProperties: Optional[Dict[str, Any]]
    limitedApplicability: Optional[List[TimePeriod]]
    zoneAuthority: List[Authority]
    dataSource: Optional[Metadata]


class TimePeriod(ImplicitDict):
    startDateTime: Optional[DateTimeType]
    endDateTime: Optional[DateTimeType]
    schedule: Optional[List[DailyPeriod]]


class DailyPeriod(ImplicitDict):
    day: List[CodeWeekDayType]
    startTime: Optional[DateTimeType]
    startEvent: Optional[CodeDaylightEventType]
    endTime: Optional[DateTimeType]
    endEvent: Optional[CodeDaylightEventType]


class Authority(ImplicitDict):
    purpose: CodeAuthorityRole
    intervalBefore: Optional[TimeInterval]
    name: Optional[List[TextShortType]]
    service: Optional[List[TextShortType]]
    contactName: Optional[List[TextShortType]]
    siteURL: Optional[TextShortType]
    email: Optional[TextShortType]
    phone: Optional[TextShortType]


class Metadata(ImplicitDict):
    creationDate: Optional[DateTimeType]
    updateDateTime: Optional[DateTimeType]
    originator: Optional[str]


class Feature(ImplicitDict):
    type: Literal["Feature"]
    id: Optional[Union[int, str]]
    properties: Optional[UASZone]
    geometry: Optional[Geometry]
    bbox: Optional[List[float]]


class ED318Schema(ImplicitDict):
    """Top-level ED-318 FeatureCollection payload."""

    type: Literal["FeatureCollection"]
    name: Optional[str]
    metadata: DatasetMetadata
    title: Optional[str]
    bbox: Optional[List[float]]
    features: List[Feature]

    @staticmethod
    def from_dict(obj: dict) -> ED318Schema:
        """Parse a raw dict into typed ED-318 classes using implicitdict."""
        return ImplicitDict.parse(obj, ED318Schema)
