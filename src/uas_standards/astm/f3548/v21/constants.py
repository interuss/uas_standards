from enum import Enum


class Scope(str, Enum):
    StrategicCoordination = "utm.strategic_coordination"
    ConstraintManagement = "utm.constraint_management"
    ConstraintProcessing = "utm.constraint_processing"
    ConformanceMonitoringForSituationalAwareness = "utm.conformance_monitoring_sa"
    AvailabilityArbitration = "utm.availability_arbitration"


AggConfMonEvaluationFlightHours = 10
AggConfMonEvaluationPeriodDays = 7
ConflictingOIMaxUserNotificationTimeSeconds = 5
ConflictingOIMaxUSSNotificationTimeSeconds = 1
CstrPublishedNotificationLatencySeconds = 5
CstrMaxAreaKm2 = 10000
CstrMaxDeletionSeconds = 5
CstrMaxDurationHours = 24
CstrMaxPlanningHorizonDays = 56
CstrMaxTimeSendDetailsSeconds = 5
CstrMaxVertices = 1000
CstrMinEffectiveTimeBufferMinutes = 10
DSSMaxSubscriptionDurationHours = 24
ExternalDataMaxRetentionTimeHours = 24
IntersectingConstraintUserNotificationMaxSeconds = 5
IntersectionMinimumPrecisionCm = 1
MaxAggConfMonAnalysisLatencyHours = 24
MaxNonPerformanceNotificationLatencyHours = 6
MaxRecoverableTimeInNonconformingStateSeconds = 60
MaxRespondToSubscriptionNotificationSeconds = 5
MaxRespondToOIDetailsRequestSeconds = 1
OiMaxCancelTimeSeconds = 5
OiMaxDurationPerExcursionSeconds = 10
OiMaxExcursionsPerFlightHour = 18
OiMaxPlanHorizonDays = 30
OiMaxUpdateRestoreConfSeconds = 5
OiMaxUpdateTimeContingentSeconds = 5
OiMaxUpdateTimeNonconfSeconds = 5
OiMaxVertices = 10000
OiMinConformancePercent = 95
PosInfoRequestMaxResponseTimeSeconds = 5
TimeSyncMaxDifferentialSeconds = 5
TimeSyncMinPercentage = 99
TransitionToEndedMaxTimeSeconds = 5
UnableToDeliverConstraintDetailsSeconds = 5
UserOiStateChangeNotificationMaxSeconds = 5
UssFunctionFailureNotificationMaxSeconds = 5
UssOiChangeNotificationMaxSeconds = 5
