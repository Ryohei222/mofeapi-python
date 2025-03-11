from dataclasses import dataclass
from typing import List

from mofeapi.enums import AggregateType


@dataclass
class TestcaseSet:
    id: int
    name: str
    points: int
    aggregate_type: AggregateType
    is_sample: bool


@dataclass
class Testcase:
    id: int
    name: str
    testcase_sets: List[bool]
