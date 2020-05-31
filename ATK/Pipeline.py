import pandas as pd
from ATK.lib import Base
from dataclasses import dataclass
from typing import Callable, List, Dict

@dataclass
class ATK_Step():
    name: str
    obj: object
    calls: List[str]
    args: List[Dict]
    completed: bool = False

class ATK_Pipeline(Base.Base):

    def __init__(self) -> None:
        self.execution_steps: List[ATK_Step] = []
        self.execution_results: List[object] = []

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def add_step(self, step: ATK_Step) -> None:
        self.execution_steps.append(step)

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def add_multiple_steps(self, steps: List[ATK_Step]):
        self.execution_steps.extend(steps)

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def run(self) -> None:
        for step in self.execution_steps:
            self.log_as.info(f'Running step "{step.name}"')
            for call, arg_dict in zip(step.calls, step.args):
                func = getattr(step.obj, call)
                func_args = arg_dict.copy()
                func_args['previous_results'] = self.execution_results[-1] if len(self.execution_results) > 0 else None
                results = func(**func_args)
                self.execution_results.append(results)
            step.completed = True
            self.log_as.info(f'Completed step "{step.name}"')