from dataclasses import dataclass
from typing import Optional


@dataclass
class Sample:
    input: str
    output: str
    explanation: Optional[str]
