from datetime import datetime
import logging
import re
from flask import url_for, request

from .. import categories, http, pages, tags
from .tag import Tag
from .page import Page
from app.utils import DictObject
from app.utils.dates import DATE_FMT

PARENS_REGEXES = [
    r'\([^)]*\)',
    r'\[[^\]]*\]',
    r'{[^}]*}',
]
BG_URL_REGEX = r'url\((https\:\/\/.*\.jpg)\)'
BORDER_REGEX = r'border-color\:(.*);'

class Gallery(DictObject):
    def __init__(self, *args, **kwargs):
        self.language = None
        self.characters = []
        self.is_translation = False
        super().__init__(*args, **kwargs)
        for tag in self.tags:
            if tag.namespace == 'language':
                if tag.value == 'translated':
                    self.is_translation = True
                elif self.language is None:
                    self.language = tag
            elif tag.namespace == 'character':
                self.characters.append(tag)
            elif tag.namespace == 'parody':
                self.parody = tag
        if ('id' not in kwargs or 'token' not in kwargs) and 'url' in kwargs:
            self.id, self.token = self.tokens_from_url(self.url)
        for page in getattr(self, 'pages', {}).values():
            page._gallery = self
        self._tags_by_namespace = None
        self._extracted_title = None
        self._extracted_artist = None
        self._full_artist = None
        self._artist = None

    @property
    def tags_by_namespaces(self):
        if not self._tags_by_namespace:
            self._tags_by_namespace = {k: [] for k in tags.NAMESPACES_ORDER}
            for tag in self.tags:
                if not tag.namespace in self._tags_by_namespace:
                    self._tags_by_namespace[tag.namespace] = []
                self._tags_by_namespace[tag.namespace].append(tag)
            self._tags_by_namespace = {k: v for k, v in self._tags_by_namespace.items() if v}
        return self._tags_by_namespace

    @property
    def extracted_title(self):
        if self._extracted_title is None:
            self._extracted_title = self.title
            for regex in PARENS_REGEXES:
                self._extracted_title = re.sub(regex, '', self._extracted_title)
        return self._extracted_title

    @property
    def extracted_artist(self):
        if self._extracted_artist is None:
            self._extracted_artist = next(
                iter(self.tags_by_namespaces.get('artist', []) + self.tags_by_namespaces.get('group', [])),
                ''
            )
        return self._extracted_artist

    @property
    def full_artist(self):
        if self._full_artist is None:
            artist = self.artist
            group = next(iter(self.tags_by_namespaces.get('group', [])), None)
            if artist and group:
                result = '{} ({})'.format(artist.value, group.value)
            else:
                result = artist or group
                if result:
                    result = result.value
            self._full_artist = result
        return self._full_artist

    @property
    def artist(self):
        if self._artist is None:
            artists = self.tags_by_namespaces.get('artist', [])
            if len(artists) != 1:
                self._artist = self.group
            else:
                self._artist = artists[0]
        return self._artist

    @property
    def group(self):
        return next(iter(self.tags_by_namespaces.get('group', [])), None)

    @property
    def group_not_artist(self):
        result = self.group
        if result == self.artist:
            return None
        return result

    @property
    def first_page(self):
        return list(self.pages.values())[0]

    @property
    def last_page(self):
        return list(self.pages.values())[-1]

    @property
    def full_url(self):
        return http.build_url(self.url)

    @classmethod
    def from_galleries_soup(cls, soup):
        panel = soup.find('td', class_='gl1e')
        main = soup.find('div', class_='gl4e')
        meta = soup.find('div', class_='gl3e')
        return cls(
            title=main.find('div', class_='glink').string,
            url=panel.find('a').get('href'),
            cover_url=panel.find('img').get('src'),
            posted_at=cls.to_time(meta.contents[1].text),
            pages_count=cls.get_pages(meta.contents[4].text),
            category=cls.get_category(meta.contents[0]),
            favorite=cls.get_favorite(meta.contents[1]),
            tags=[Tag.from_str(x.get('title')) for x in cls.find_tags(main)],
            rating=cls.get_rating(meta.contents[2]),
        )

    @classmethod
    def from_gallery_soup(cls, soup, *args, **kwargs):
        main = soup.find('div', class_='gm')
        meta = soup.find('div', id='gd3')
        meta_list = [
            x.contents[1] for
            x in meta.find('div', id='gdd').find_all('tr')
        ]
        pages = soup.find('div', id='gdt')
        if meta_list[1].text == 'None':
            parent_url = None
        else:
            id, token = cls.tokens_from_url(meta_list[1].find('a').get('href'))
            parent_url = url_for('.gallery', id=id, token=token)
        return cls(
            **kwargs,
            title=main.find('h1', id='gn').text,
            cover_url=cls.get_background(main.find('div', id='gd1').find('div')),
            posted_at=cls.to_time(meta_list[0].text),
            pages_count=cls.get_pages(meta_list[5].text),
            pages={
                p.page: p
                for p in [
                    Page.from_url_str(
                        x.find('div').find('a').get('href'),
                        style=x.find('div').get('style')
                    ) if x.find('div') else
                    Page.from_link_with_img(x.find('a'))
                    for x in (
                        pages.find_all('div', class_='gdtm') +
                        pages.find_all('div', class_='gdtl')
                    )
                ]
            },
            language=Tag.language(meta_list[3].text.split(' ')[0]),
            category=cls.get_category(meta.find('div', id='gdc').find('div')),
            tags=[Tag.from_str(x.get('id')[3:]) for x in cls.find_tags(main)],
            parent_url=parent_url,
            rating=cls.get_rating(meta.find('div', id='rating_image')),
            rating_count=int(meta.find('span', id='rating_count').text),
            file_size=meta_list[4].text,
            uploader=meta.find('div', id='gdn').find('a').text,
        )

    @classmethod
    def from_id(cls, id, token, page=None, has_pages=[]):
        logging.debug('Creating gallery from ID')
        page = (page or http.get_page()) - 1
        missing = []
        url=pages.GALLERY_ROUTE.format(id=id, token=token, page=page)
        logging.debug('Requesting base gallery')
        result = cls.from_gallery_soup(
            http.to_soup(http.call(url).content),
            id=id, token=token, url=url,
        )
        is_large = result.first_page.type == 'image'
        for page in has_pages:
            page = (page - 1) // (20 if is_large else 40)
            if page not in missing and page > (0 if is_large else 1):
                missing.append(page)
        urls = [
            pages.GALLERY_ROUTE.format(id=id, token=token, page=page)
            for page in missing
        ]
        logging.debug('Requesting additional gallery pages {}'.format(missing))
        for url in urls:
            result.pages.update(
                cls.from_gallery_soup(
                    http.to_soup(http.call(url).content),
                    url=url,
                ).pages
            )
        return result

    @classmethod
    def get_galleries_from_root(cls, soup):
        table = soup.find(class_=['itg', 'glte'])
        if not table:
            return []
        return [cls.from_galleries_soup(x) for x in table.contents if x.find(class_='gl1e')]

    @classmethod
    def get_galleries(cls, url=pages.GALLERIES_SEARCH_ROUTE, page=1, filters=None):
        filters = http.get_filters() if filters is None else filters
        response = http.call(url.format(
            page=page - 1,
            search=request.args.get('search', ''),
            category_filter=categories.to_filter(filters)
        ))
        return cls.get_galleries_from_root(http.to_soup(response.content))

    @staticmethod
    def get_rating(soup):
        """
        Calculates the rating from the soup rating style
        """
        style = soup.get('style')
        x, y = style.split(':')[1].split(';')[0].split(' ')
        x = int(x[1:3]) if x[0] == '-' else 0
        result = 5
        result -= x / (64 / 4)
        if y == '-21px':
            result -= .5
        return result

    @staticmethod
    def find_tags(soup):
        """
        Finds the gallery tags in a soup
        """
        return soup.find_all('div', class_='gtl') + soup.find_all('div', class_='gt')

    @staticmethod
    def to_time(text):
        """
        Converts gallery date text to datetime
        """
        return datetime.strptime(text, DATE_FMT)

    @staticmethod
    def get_pages(text):
        return int(text.split(' ')[0])

    @staticmethod
    def tokens_from_url(url):
        return url.split('/')[-3:-1]

    @staticmethod
    def get_category(soup):
        return soup.text.lower().replace(' ', '')

    @staticmethod
    def get_background(soup):
        match = re.search(BG_URL_REGEX, soup.get('style'))
        if not match:
            return None
        return match.group(1)

    @staticmethod
    def get_favorite(soup):
        match = re.search(BORDER_REGEX, soup.get('style', ''))
        if not match:
            return None
        return match.group(1)
