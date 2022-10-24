from dataclasses import dataclass


@dataclass
class Preview:
    url: str
    page: int
    page_token: str
    width: int
    height: int
    offset_x: int = 0
