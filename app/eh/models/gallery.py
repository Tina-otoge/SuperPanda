import typing as t
from dataclasses import dataclass
from datetime import datetime

from .category import Category


@dataclass
class Gallery:
    id: int
    token: str

    title: str
    category: Category

    pages_count: int
    created_at: datetime
    uploader: str

    tags: list[str]

    title_orig: str = None
    cover_url: str = None
