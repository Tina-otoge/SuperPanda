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

    def get_tags_by_namespace(self):
        tags_by_namespace = {}
        for tag in self.tags:
            namespace, value = tag.split(":", 1)
            tags_by_namespace.setdefault(namespace, []).append(value)
        return tags_by_namespace

    @property
    def smart_title(self) -> str:
        bracket_pos = self.title.find("]")
        if (
            self.title[0] not in ("[", "(")
            or bracket_pos == -1
            or bracket_pos == len(self.title) - 1
        ):
            return self.title
        return self.title[bracket_pos + 1 :].strip()

    @property
    def smart_artist(self) -> str:
        tags = self.get_tags_by_namespace()
        artists = tags.get("artist")
        if not artists:
            return ""
        if len(artists) == 1:
            return artists[0]
        groups = tags.get("group")
        if groups and len(groups) == 1:
            return groups[0]
        return ", ".join(artists)

    @property
    def smart_language(self) -> str:
        tags = self.get_tags_by_namespace()
        languages = tags.get("language")
        if not languages:
            return ""
        append = [""]
        if "translated" in languages:
            languages.remove("translated")
            append.append("(TR)")
        if "rewrite" in languages:
            languages.remove("rewrite")
            append.append("(RW)")
        return ", ".join(languages) + " ".join(append)
