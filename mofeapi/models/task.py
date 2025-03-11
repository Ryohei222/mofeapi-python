from dataclasses import dataclass
from typing import List, Optional

from mofeapi.enums import Difficulty
from mofeapi.models.sample import Sample


@dataclass
class Task:
    slug: str
    name: str
    position: str
    difficulty: Difficulty
    accepted: bool
    points: int
    execution_time_limit: Optional[int]


@dataclass
class TaskDetail(Task):
    input_format: str
    output_format: str
    statement: str
    constraints: str
    partial_scores: str
    samples: List[Sample]
