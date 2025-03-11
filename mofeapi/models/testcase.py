from dataclasses import dataclass
from typing import List, Optional

from mofeapi.enums import AggregateType


@dataclass
class TestcaseSetBase:
    aggregate_type: AggregateType
    name: str
    points: int


@dataclass
class TestcaseSet(TestcaseSetBase):
    id: int
    is_sample: bool


@dataclass
class Testcase:
    id: int
    name: str
    testcase_sets: List[bool]


@dataclass
class TestcaseParams:
    name: str
    input: str
    output: str
    explanation: str


@dataclass
class TestcaseDetail:
    id: int
    name: str
    input: str
    output: str
    explanation: Optional[str]
