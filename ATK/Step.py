from typing import List, Dict
from dataclasses import dataclass, field

from ATK.lib.Enums import StepName


@dataclass
class Step():
    name: StepName
    obj: object
    calls: List[str]
    args: List[Dict]
    prereqs: List[StepName] = field(default_factory=list)
    completed: bool = False