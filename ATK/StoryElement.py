from dataclasses import dataclass

from ATK.lib.Enums import SlideType


@dataclass
class StoryElement():
    transcript: str
    slide: int
    next_slide: int
    type: SlideType
    is_cached: bool = False

    def view(self) -> str:
        return self.transcript
