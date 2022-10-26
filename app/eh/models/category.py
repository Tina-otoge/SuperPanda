class _CategoryMeta(type):
    def __getattr__(cls, name):
        return cls.subclasses[name.lower()]


class Category(metaclass=_CategoryMeta):
    color = None
    color2 = None
    value = None

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    @classmethod
    @property
    def subclasses(cls):
        return {c.__name__.lower(): c for c in cls.__subclasses__()}

    @classmethod
    def from_str(cls, s):
        s = s.lower().replace(" ", "").replace("-", "")
        category = cls.subclasses.get(s)
        if not category:
            raise ValueError("Invalid category: {}".format(s))
        return category

    @classmethod
    def compute(cls, *categories):
        return 1023 - sum([c.value for c in categories])


class Misc(Category):
    color = "#707070"
    color2 = "#9e9e9e"
    value = 1


class Doujinshi(Category):
    color = "#fc4e4e"
    color2 = "#f26f5f"
    value = 2


class Manga(Category):
    color = "#e78c1a"
    color2 = "#fcb417"
    value = 4


class ArtistCG(Category):
    color = "#c7bf07"
    color2 = "#dde500"
    value = 8
    name = "Artist CG"


class GameCG(Category):
    color = "#1a9317"
    color2 = "#05bf0b"
    value = 16
    name = "Game CG"


class ImageSet(Category):
    color = "#2756aa"
    color2 = "#5f5fff"
    value = 32
    name = "Image Set"


class Cosplay(Category):
    color = "#8800c3"
    color2 = "#9755f5"
    value = 64


class AsianPorn(Category):
    color = "#b452a5"
    color2 = "#fe93ff"
    value = 128
    name = "Asian Porn"


class NonH(Category):
    color = "#0f9ebd"
    color2 = "#08d7e2"
    value = 256
    name = "Non-H"


class Western(Category):
    color = "#5dc13b"
    color2 = "#14e723"
    value = 512


class Private(Category):
    pass
