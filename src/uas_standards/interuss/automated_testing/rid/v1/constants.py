from enum import Enum


class Scope(str, Enum):
    Inject = "rid.inject_test_data"
    Observe = "dss.read.identification_service_areas"
