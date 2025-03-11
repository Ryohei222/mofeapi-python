from typing import Dict, List, Any, Optional
from mofeapi.enums import Difficulty
from mofeapi.models.task import Task
from mofeapi.constants import DEFAULT_DIFFICULTY
from mofeapi.models.sample import Sample
from mofeapi.models.contest import Contest, ContestBase


class ProblemBase:
    """
    export interface ProblemBase {
        name: string
        difficulty: Difficulty
    }
    """
    def __init__(self, name: str, difficulty: Difficulty):
        self.name = name
        self.difficulty = difficulty

class Problem(ProblemBase):
    '''
    export interface Problem extends ProblemBase {
        id: number
        writerUser: string
        contest: null | {
            slug: string
            name: string
        }
    }
    '''
    def __init__(self, name: str, difficulty: Difficulty, id: int, writer_user: str, contest: Optional[ContestBase] = None):
        super().__init__(name, difficulty)
        self.id = id
        self.writer_user = writer_user
        self.contest = contest

    def __repr__(self):
        return str(self.__dict__)

class ProblemDetail:
    '''
    export interface ProblemDetail {
        id: number
        slug: string | null
        executionTimeLimit: number
        name: string
        difficulty: Difficulty
        writerUser: string
        statement: string
        constraints: string
        partialScores: string | null
        inputFormat: string
        outputFormat: string
        checkerPath: string | null
        samples: Sample[] | null
        testers: string[]
        contest: Contest | null
        submissionLimit1: number | null
        submissionLimit2: number | null
    }
    '''
    def __init__(self, id: int, execution_time_limit:int , name: str, difficulty: Difficulty, writer_user: str, statement: str, constraints: str, input_format: str, output_format: str, testers: List[str], slug: Optional[str], partial_scores: Optional[str] = None, checker_path: Optional[str] = None, samples: Optional[List[Sample]] = None, contest: Optional[Contest] = None, submission_limit_1: Optional[int] = None, submission_limit_2: Optional[int] = None):
        self.id = id
        self.execution_time_limit = execution_time_limit
        self.name = name
        self.difficulty = difficulty
        self.writer_user = writer_user
        self.statement = statement
        self.constraints = constraints
        self.input_format = input_format
        self.output_format = output_format
        self.testers = testers
        self.slug = slug
        self.partial_scores = partial_scores
        self.checker_path = checker_path
        self.samples = samples
        self.contest = contest
        self.submission_limit_1 = submission_limit_1
        self.submission_limit_2 = submission_limit_2
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProblemDetail':
        return cls(
            id=data.get('id'),
            execution_time_limit=data.get('execution_time_limit'),
            name=data.get('name'),
            difficulty=Difficulty._value2member_map_[data.get('difficulty')],
            writer_user=data.get('writer_user'),
            statement=data.get('statement'),
            constraints=data.get('constraints'),
            input_format=data.get('input_format'),
            output_format=data.get('output_format'),
            testers=data.get('testers', []),
            slug=data.get('slug', None),
            partial_scores=data.get('partial_scores', None),
            checker_path=data.get('checker_path', None),
            samples=[Sample.from_dict(sample) for sample in data.get('samples')] if data.get('samples') else None,
            contest=Contest.from_dict(data.get('contest')) if data.get('contest') else None,
            submission_limit_1=data.get('submission_limit_1', None),
            submission_limit_2=data.get('submission_limit_2', None),
        )