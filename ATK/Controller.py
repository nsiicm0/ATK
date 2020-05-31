from ATK.lib import Base
from ATK.Pipeline import ATK_Pipeline

class ATK_Controller(Base.Base):

    def __init__(self) -> None:
        self.pipeline: ATK_Pipeline = ATK_Pipeline()

    @Base.wrap(pre=Base.entering, post=Base.exiting, guard=False)
    def main(self):
        pass