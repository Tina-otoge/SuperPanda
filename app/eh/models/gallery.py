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
    first_page_token: str = None

    def get_tags_by_namespace(self):
        namespaces = {
            x: []
            for x in (
                "artist",
                "group",
                "language",
                "parody",
                "character",
                "female",
                "male",
                "other",
            )
        }
        for tag in self.tags:
            namespace, value = tag.split(":", 1)
            if namespace not in namespaces:
                namespace = "other"
            namespaces[namespace].append(value)
        return namespaces

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
    def artists(self) -> list[str]:
        return self.get_tags_by_namespace()["artist"]

    @property
    def groups(self) -> list[str]:
        return self.get_tags_by_namespace()["group"]

    @property
    def smart_artist(self) -> str:
        if not self.artists:
            return ", ".join(self.groups)
        if len(self.artists) == 1:
            return self.artists[0]
        if self.groups and len(self.groups) == 1:
            return self.groups[0]
        return ", ".join(self.artists)

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

    @property
    def smart_title_orig(self) -> str:
        if self.title_orig == self.title:
            return ""
        title = self.title_orig or self.title
        if title == self.smart_title:
            return ""
        return title

    @property
    def artist_full(self) -> str:
        if not self.artists:
            return ", ".join(self.groups)
        s = ", ".join(self.artists)
        if self.groups:
            s += " " + ", ".join(self.groups)
        return s
