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
