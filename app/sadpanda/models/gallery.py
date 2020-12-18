from datetime import datetime

from .tag import Tag
from app.utils import DictObject
from app.utils.dates import DATE_FMT
from app.utils.html import get_gallery_page

class Gallery(DictObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.characters = []
        self.translation = False
        for tag in self.tags:
            if tag.namespace == 'language':
                if tag.value == 'translated':
                    self.translation = True
                else:
                    self.language = tag
            elif tag.namespace == 'character':
                self.characters.append(tag)
            elif tag.namespace == 'parody':
                self.parody = tag

    @staticmethod
    def rating_from_soup(soup):
        style = soup.get('style')
        x, y = style.split(':')[1].split(';')[0].split(' ')
        x = int(x[1:3]) if x[0] == '-' else 0
        result = 5
        result -= x / (64 / 4)
        if y == '-21px':
            result -= .5
        return result

    @classmethod
    def from_soup(cls, soup):
        panel = soup.find('td', class_='gl1e')
        main = soup.find('div', class_='gl4e')
        meta = soup.find('div', class_='gl3e')
        return cls(
            title=main.find('div', class_='glink').string,
            link_url=panel.find('a').get('href'),
            cover_url=panel.find('img').get('src'),
            posted_at=datetime.strptime(meta.contents[1].text, DATE_FMT),
            pages=int(meta.contents[4].text.split(' ')[0]),
            category=meta.contents[0].get('onclick').split('/')[-1][:-1],
            tags=[
                Tag.from_str(x.get('title')) for x in
                main.find_all('div', class_='gtl') + main.find_all('div', class_='gt')
            ],
            rating=cls.rating_from_soup(meta.contents[2]),
        )

    @classmethod
    def get_galleries_from_root(cls, soup):
        table = soup.find(class_=['itg', 'glte'])
        return [cls.from_soup(x) for x in table.contents if x.find(class_='gl1e')]

    @classmethod
    def get_galleries(cls):
        soup = get_gallery_page()
        return cls.get_galleries_from_root(soup)
