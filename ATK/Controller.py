from ATK.lib import Base
from ATK.Pipeline import Pipeline

class Controller(Base.Base):

    def __init__(self) -> None:
        self.pipeline: Pipeline = Pipeline()

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def main(self):
        pass