from dataclasses import dataclass
from typing import List, Optional, Union

from mofeapi.enums import Difficulty
from mofeapi.models.contest import Contest, ContestBase
from mofeapi.models.sample import Sample

# Reference:
# https://github.com/mofecoder/mofe-front/blob/master/app/types/problems.ts


@dataclass
class ProblemBase:
    name: str
    difficulty: Difficulty


@dataclass
class Problem:
    name: str
    difficulty: Difficulty
    id: int
    writer_user: str
    contest: Optional[ContestBase]


@dataclass
class ProblemDetail:
    id: int
    execution_time_limit: int
    name: str
    difficulty: Difficulty
    writer_user: str
    statement: str
    constraints: str
    input_format: str
    output_format: str
    testers: List[str]
    slug: Optional[str]
    partial_scores: Optional[str]
    checker_path: Optional[str]
    samples: Optional[List[Sample]]
    contest: Optional[Contest]
    submission_limit_1: Optional[int]
    submission_limit_2: Optional[int]


@dataclass
class ProblemParams:
    name: str
    difficulty: Difficulty
    statement: str
    input_format: str
    output_format: str
    constraints: str
    execution_time_limit: int
    partial_scores: Optional[str]
    submission_limit_1: Optional[Union[int, str]]
    submission_limit_2: Optional[Union[int, str]]
