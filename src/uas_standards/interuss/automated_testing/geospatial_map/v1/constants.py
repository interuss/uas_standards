from enum import Enum


class Scope(str, Enum):
    DirectAutomatedTest = "interuss.geospatial_map.direct_automated_test"
    Query = "interuss.geospatial_map.query"
