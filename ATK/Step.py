from typing import List, Dict
from dataclasses import dataclass, field


@dataclass
class Step():
    name: str
    obj: object
    calls: List[str]
    args: List[Dict]
    prereqs: List[str] = field(default_factory=list)
    completed: bool = False