from dataclasses import dataclass
from typing import Dict, List, Optional

from mofeapi.enums import SubmissionResult as Result
from mofeapi.models.task import Task


@dataclass
class User:
    name: str


@dataclass
class Submit:
    id: int
    timestamp: str
    user: User
    task: Task
    status: Result
    lang: str
    execution_time: Optional[int]
    execution_memory: Optional[int]
    point: int
    public: bool
    judge_status: Optional[Dict[str, int]]


@dataclass
class TestcaseResult:
    testcase_name: Optional[str]
    status: Result
    execution_time: int
    execution_memory: int
    score: Optional[int] = None


@dataclass
class TestcaseSetResult:
    name: str
    score: int
    point: int
    testcases: Optional[List[str]]
    results: Dict[str, int]


@dataclass
class SubmissionDetail(Submit):
    source: str
    sample_count: Optional[int]
    compile_error: Optional[str]
    permission: bool
    testcase_results: List[TestcaseResult]
    testcase_sets: List[TestcaseSetResult]
