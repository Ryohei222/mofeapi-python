from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from mofeapi.enums import ContestKind, StandingsMode
from mofeapi.models.task import Task


@dataclass
class ContestBase:
    slug: str
    name: str


@dataclass
class Contest:
    slug: str
    name: str
    kind: ContestKind
    start_at: str
    end_at: str


@dataclass
class ContestDetail:
    slug: str
    name: str
    kind: ContestKind
    start_at: str
    end_at: str
    description: str
    penalty_time: int
    is_writer_or_tester: bool
    written_tasks: List[Dict[str, Any]]
    is_admin: bool
    standings_mode: StandingsMode
    registration_restriction: bool
    allow_open_registration: bool
    allow_team_registration: bool
    tasks: Optional[List[Task]]
    registered: Optional[Dict[str, Any]]
    editorial: Optional[str]


@dataclass
class ContestEditParam:
    name: Optional[str]
    kind: Optional[ContestKind]
    start_at: Optional[str]
    end_at: Optional[str]
    description: Optional[str]
    penalty_time: Optional[int]
    editorial_url: Optional[str]
    official_mode: Optional[bool]
    standings_mode: Optional[StandingsMode]
    closed_password: Optional[str]
    allow_team_registration: Optional[bool]
    allow_open_registration: Optional[bool]
