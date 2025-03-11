from typing import Dict, List, Any, Optional
from mofeapi.enums import Difficulty
from mofeapi.constants import DEFAULT_DIFFICULTY
from mofeapi.models.sample import Sample

class Task:
    def __init__(self, slug: str, name: str, position: str, difficulty: Difficulty, accepted: bool, points: int, execution_time_limit: int):
        self.slug = slug
        self.execution_time_limit = execution_time_limit
        self.position = position
        self.name = name
        self.difficulty = difficulty
        self.points = points
        self.accepted = accepted
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        return cls(
            slug=data.get('slug'),
            execution_time_limit=data.get('execution_time_limit'),
            position=data.get('position'),
            name=data.get('name'),
            difficulty=Difficulty._value2member_map_[data.get('difficulty')],
            accepted=data.get('accepted'),
            points=data.get('points'),
        )

class TaskDetail(Task):
    def __init__(self, slug: str, name: str, position: str, difficulty: Difficulty, accepted: bool, points: int, execution_time_limit: int, input_format: str, output_format:str , statement: str, constraints :str, partial_scores: str,  samples: List[Sample]):
        super().__init__(slug, name, position, difficulty, accepted, points, execution_time_limit)
        self.statement = statement
        self.output_format = output_format
        self.input_format = input_format
        self.constraints = constraints
        self.partial_scores = partial_scores
        self.samples = samples
    
    def __repr__(self):
        return str(self.__dict__)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskDetail':
        return cls(
            slug=data.get('slug'),
            name=data.get('name'),
            position=data.get('position'),
            difficulty=Difficulty._value2member_map_[data.get('difficulty')],
            accepted=data.get('accepted'),
            points=data.get('points'),
            constraints=data.get('constraints'),
            execution_time_limit=data.get('execution_time_limit'),
            input_format=data.get('input_format'),
            output_format=data.get('output_format'),
            statement=data.get('statement'),
            samples=[Sample.from_dict(sample) for sample in data.get('samples', [])]
        )