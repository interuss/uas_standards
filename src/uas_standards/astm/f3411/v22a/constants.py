from enum import Enum


class Scope(str, Enum):
    DisplayProvider = "rid.display_provider"
    ServiceProvider = "rid.service_provider"


NetMinUasLocRefreshFrequencyHz = 1
NetMinUasLocRefreshPercentage = 20
NetMaxDisplayAreaDiagonalKm = 7
NetSpDataResponseTime95thPercentileSeconds = 1
NetSpDataResponseTime99thPercentileSeconds = 3
NetMaxNearRealTimeDataPeriodSeconds = 60
NetDpMaxDataRetentionPeriodSeconds = 86400
NetDpInitResponse95thPercentileSeconds = 6
NetDpInitResponse99thPercentileSeconds = 18
NetDpDataResponse95thPercentileSeconds = 1
NetDpDataResponse99thPercentileSeconds = 3
NetMinSessionLengthSeconds = 5
NetDpDetailsResponse95thPercentileSeconds = 2
NetDpDetailsResponse99thPercentileSeconds = 6
NetDetailsMaxDisplayAreaDiagonalKm = 2
NetMinClusterSizePercent = 15
NetMinObfuscationDistanceM = 300
NetDSSMaxSubscriptionPerArea = 10
NetDSSMaxSubscriptionDurationHours = 24

MinPositionResolution = 0.0000001
"""Minimum resolution of both latitude and longitude values, in degrees, according to definitions in Table 1."""

MaxSpeed = 254.25
"""Maximum value for ground speed of flight, in meters per second, according to definitions in Table 1."""

SpecialSpeed = 255
"""Special value for ground speed of flight indicating Invalid, No Value or Unknown, according to definitions in Table 1."""

MinSpeedResolution = 0.25
"""Minimum resolution of ground speed of flight value, in in meters per second, according to definitions in Table 1."""

MaxAbsVerticalSpeed = 62
"""Maximum for vertical speed upward relative to the WGS-84 datum absolute value, in in meters per second, according to definitions in Table 1."""

SpecialVerticalSpeed = 63
"""Special value for vertical speed indicating Invalid, No Value or Unknown, according to definitions in Table 1."""

MinHeightResolution = 1
"""Minimum resolution of height value, in meters, according to definitions in Table 1."""

SpecialHeight = -1000
"""Special value for height indicating Invalid, No Value or Unknown, according to definitions in Table 1."""

MinTrackDirection = -359
"""Minimum value for track direction, in degrees, according to definitions in Table 1."""

MaxTrackDirection = 359
"""Maximum value for track direction, in degrees, according to definitions in Table 1."""

SpecialTrackDirection = 361
"""Special value for track direction indicating Invalid, No Value or Unknown, according to definitions in Table 1."""

MinTrackDirectionResolution = 1
"""Minimum resolution of track direction value, in degrees, according to definitions in Table 1."""
