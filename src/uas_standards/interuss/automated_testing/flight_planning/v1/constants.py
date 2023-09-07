from enum import Enum


class Scope(str, Enum):
    DirectAutomatedTest = "interuss.flight_planning.direct_automated_test"
    Plan = "interuss.flight_planning.plan"
