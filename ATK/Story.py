from typing import List

from ATK.lib import Base
from ATK.StoryElement import StoryElement

from ATK.lib.Exceptions import StoryInvalidElementPassedException


class Story(Base.Base):

    def __init__(self) -> None:
        self._lines = []

    def get_lines(self):
        return self._lines

    def add_line(self, element: StoryElement) -> None:
        if isinstance(element, StoryElement):
            self._lines.append(element)
        else:
            raise StoryInvalidElementPassedException('Invalid element passed. Element has to be of type ATK_Story_Element.')

    def add_lines(self, elements: List[StoryElement]) -> None:
        if all(isinstance(element, StoryElement) for element in elements):
            self._lines.extend(elements)
        else:
            raise StoryInvalidElementPassedException('Invalid elements passed. Elements have to be of type ATK_Story_Element.')

    def tell_slide(self, slide: int) -> List[StoryElement]:
        return list(filter(lambda line: line.slide == slide, self._lines))

