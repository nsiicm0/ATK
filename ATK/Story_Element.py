from dataclasses import dataclass


@dataclass
class ATK_Story_Element():
    transcript: str
    slide: int
    file_path: str
    is_cached: bool = False