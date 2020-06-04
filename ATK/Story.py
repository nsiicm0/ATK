from typing import List

from ATK.Story_Element import ATK_Story_Element
from ATK.lib import Base

from ATK.lib.Exceptions import ATK_Story_Invalid_Element_Passed_Exception


class ATK_Story(Base.Base):

    def __init__(self) -> None:
        self._lines = []

    def get_lines(self):
        return self._lines

    def add_line(self, element: ATK_Story_Element):
        if isinstance(element, ATK_Story_Element):
            self._lines.append(element)
        else:
            raise ATK_Story_Invalid_Element_Passed_Exception('Invalid element passed. Element has to be of type ATK_Story_Element.')

    def add_lines(self, elements: List[ATK_Story_Element]):
        if all(isinstance(element, ATK_Story_Element) for element in elements):
            self._lines.extend(elements)
        else:
            raise ATK_Story_Invalid_Element_Passed_Exception('Invalid elements passed. Elements have to be of type ATK_Story_Element.')
