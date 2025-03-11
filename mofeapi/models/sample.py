from typing import Dict

class Sample:
    def __init__(self, input: str, output: str, explanation: str):
        self._input = input
        self._output = output
        self._explanation = explanation

    def __repr__(self):
        return str(self.__dict__)
    
    @property
    def input(self) -> str:
        return self._input
    @property
    def output(self) -> str:
        return self._output
    @property
    def explanation(self) -> str:
        return self._explanation
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Sample':
        explanation = data.get('explanation')
        if explanation is None:
            explanation = ''
        return cls(
            input=data.get('input'),
            output=data.get('output'),
            explanation=explanation
        )