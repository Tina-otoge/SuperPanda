import enum


class Category(enum.Enum):
    DOUJINSHI = enum.auto()
    MANGA = enum.auto()
    ARTIST_CG = enum.auto()
    GAME_CG = enum.auto()
    NON_H = enum.auto()
    IMAGE_SET = enum.auto()
    WESTERN = enum.auto()
    COSPLAY = enum.auto()
    MISC = enum.auto()
    PRIVATE = enum.auto()

    @classmethod
    def from_str(cls, s):
        try:
            return cls[s.upper().replace(" ", "_").replace("-", "_")]
        except KeyError:
            raise ValueError(f"Invalid category: {s}")
