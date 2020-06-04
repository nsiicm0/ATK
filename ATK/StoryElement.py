from dataclasses import dataclass


@dataclass
class StoryElement():
    transcript: str
    slide: int
    next_slide: int
    file_path: str
    is_cached: bool = False