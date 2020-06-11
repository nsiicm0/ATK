import os
import pickle
from ATK.Step import Step
from ATK.lib import Base
from typing import List

from ATK.lib.Exceptions import PipelineDependencyException

class Pipeline(Base.Base):

    def __init__(self, config) -> None:
        self.execution_steps: List[Step] = []
        self.execution_results: List[object] = []
        self.already_executed: List[str] = []
        self.config = config

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def add_step(self, step: Step) -> None:
        self.execution_steps.append(step)

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def add_multiple_steps(self, steps: List[Step]):
        self.execution_steps.extend(steps)

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def check_prereqs(self, depends_on: str) -> bool:
        return depends_on in self.already_executed

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def run(self) -> None:
        uid = self.config['UID']
        self.log_as.info(f'Running pipeline for "{uid}"')
        for step in self.execution_steps:
            self.log_as.info(f'Running step "{step.name}"')
            # check for prereqs
            if all(self.check_prereqs(req) for req in step.prereqs) or len(step.prereqs) == 0:
                for call, arg_dict in zip(step.calls, step.args):
                    func = getattr(step.obj, call)
                    func_args = dict({**arg_dict, **self.config})
                    if len(self.execution_results) > 0 and len(step.prereqs) > 0:
                        func_args['dependent_results'] = list(filter(lambda res: any(map(lambda pre: res['step'].startswith(pre.value),step.prereqs)), self.execution_results))
                    results = func(**func_args)
                    self.execution_results.append(dict({'step': f'{step.name.value}_{call}', 'results': results}))
                step.completed = True
                self.already_executed.append(step.name)
                self.log_as.info(f'Completed step "{step.name}"')
            else:
                raise PipelineDependencyException('A prerequisit for this step was not met.')
        dest_path = os.path.join('.', self.config['BKP_DIR'], uid)
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        pickle_name = os.path.join(dest_path, f'{uid}.results.obj')
        with open(pickle_name, 'wb') as fp:
            pickle.dump(self.execution_results, fp)