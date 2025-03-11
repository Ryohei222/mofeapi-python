from mofeapi.enums import AggregateType
from typing import Dict, Any, List

class TestcaseSet:
    '''
    export interface TestcaseSet {
        id: number
        name: string
        points: number
        aggregateType: AggregateType
        isSample: boolean
    }
    '''
    def __init__(self, id: int, name: str, points: int, aggregate_type: AggregateType, is_sample: bool):
        self.id = id
        self.name = name
        self.points = points
        self.aggregate_type = aggregate_type
        self.is_sample = is_sample
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestcaseSet':
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            points=data.get('points'),
            aggregate_type=AggregateType._value2member_map_[data.get('aggregate_type')],
            is_sample=data.get('is_sample')
        )

class Testcase:
    '''
    export interface Testcase {
        id: number
        name: string
        testcaseSets: boolean[]
    }
    '''
    def __init__(self, id: int, name: str, testcase_sets: List[bool]):
        self.id = id
        self.name = name
        self.testcase_sets = testcase_sets

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Testcase':
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            testcase_sets=data.get('testcase_sets')
        )