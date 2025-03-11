from typing import Dict, List, Optional, Any
from mofeapi.enums import StandingsMode, ContestKind
from mofeapi.models.task import Task

class ContestBase:
    def __init__(self, slug: str, name: str):
        self.slug = slug
        self.name = name

class Contest:
    def __init__(self, slug: str, name: str, kind: ContestKind, start_at: str, end_at: str):
        self.slug = slug
        self.name = name
        self.kind = kind
        self.start_at = start_at
        self.end_at = end_at

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Contest':
        return cls(
            slug=data.get('slug'),
            name=data.get('name'),
            kind=ContestKind._value2member_map_[data.get('kind')],
            start_at=data.get('start_at'),
            end_at=data.get('end_at')
        )

class ContestDetail(Contest):
    def __init__(self, slug: str, name: str, kind: ContestKind, start_at: str, end_at: str,
                 description: str, penalty_time: int, is_writer_or_tester: bool, written_tasks: List[Dict[str, Any]],
                 is_admin: bool, standings_mode: StandingsMode, registration_restriction: bool, allow_open_registration: bool, allow_team_registration: bool,
                 tasks: Optional[List[Task]] = None, registered: Optional[Dict[str, Any]] = None, editorial: Optional[str] = None):
        super().__init__(slug, name, kind, start_at, end_at)
        self.tasks = tasks if tasks is not None else []
        self.description = description
        self.penalty_time = penalty_time
        self.is_writer_or_tester = is_writer_or_tester
        self.registered = registered # registered: { name: string | null; open: boolean } | null
        self.editorial = editorial
        self.written_tasks = written_tasks if written_tasks is not None else []
        self.is_admin = is_admin
        self.standings_mode = standings_mode
        self.registration_restriction = registration_restriction
        self.allow_open_registration = allow_open_registration
        self.allow_team_registration = allow_team_registration
    
    def __repr__(self):
        return str(self.__dict__)

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> 'ContestDetail':
        if data is None:
            return cls(None, None, None, None, None)
            
        tasks = []
        if 'tasks' in data and data['tasks'] is not None:
            tasks = [Task.from_dict(task_data) for task_data in data['tasks']]
            
        written_tasks = []
        if 'written_tasks' in data and data['written_tasks'] is not None:
            written_tasks = data['written_tasks']
            
        return cls(
            slug=data.get('slug'),
            name=data.get('name'),
            kind=data.get('kind'),
            start_at=data.get('start_at'),
            end_at=data.get('end_at'),
            description=data.get('description'),
            penalty_time=data.get('penalty_time'),
            tasks=tasks,
            is_writer_or_tester=data.get('is_writer_or_tester'),
            registered=data.get('registered'),
            editorial=data.get('editorial'),
            written_tasks=written_tasks,
            is_admin=data.get('is_admin'),
            standings_mode= StandingsMode._value2member_map_[data.get('standings_mode')],
            registration_restriction=data.get('registration_restriction'),
            allow_open_registration=data.get('allow_open_registration'),
            allow_team_registration=data.get('allow_team_registration')
        )
    
class ContestEditParam:
    def __init__(self, name: Optional[str] = None, kind: Optional[ContestKind] = None, start_at: Optional[str] = None, end_at: Optional[str] = None,
                 description: Optional[str] = None, penalty_time: Optional[int] = None, editorial_url: Optional[str] = None,
                 official_mode: Optional[bool] = None, standings_mode: Optional[StandingsMode] = None, closed_password: Optional[str] = None,
                 allow_team_registration: Optional[bool] = None, allow_open_registration: Optional[bool] = None):
        self.name = name
        self.kind = kind
        self.start_at = start_at
        self.end_at = end_at
        self.description = description
        self.penalty_time = penalty_time
        self.editorial_url = editorial_url
        self.official_mode = official_mode
        self.standings_mode = standings_mode
        self.closed_password = closed_password
        self.allow_team_registration = allow_team_registration
        self.allow_open_registration = allow_open_registration