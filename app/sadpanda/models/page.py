from flask import url_for

from .. import http, pages

class Page:
    def __init__(self, gallery=None, token=None, page=None, style=None):
        self.gallery = gallery
        self.token = token
        self.page = page
        self.style = style
        self.loaded = False
        self._gallery = None
        self._image = None
        self._prev = None
        self._prev_style = None
        self._next = None
        self._next_style = None
        self._gallery_token = None

    def __repr__(self):
        return '<{0.__class__.__name__}: {1}>'.format(self, str(self))

    def __str__(self):
        return '{0.gallery}#{0.page}'.format(self)

    def to_json(self):
        return self.url

    @property
    def url(self):
        return pages.GALLERY_PAGE_URL.format(
            token=self.token, gallery=self.gallery, page=self.page
        )

    @property
    def reader_url(self):
        return url_for(
            'main.reader',
            gallery=self.gallery, token=self.token, page=self.page
        )

    def load(self):
        if not self.loaded:
            from .gallery import Gallery
            soup = http.to_soup(http.session.get(self.url).content)
            self._image = soup.find('img', id='img').get('src')
            self._prev = self.__class__.from_str(soup.find('a', id='prev').get('href'))
            self._next = self.__class__.from_str(soup.find('a', id='next').get('href'))
            self._gallery_token = self.get_gallery_token(
                soup.find('div', id='i5').find('a')
            )
            self._gallery = Gallery.get_gallery_from_id_token(
                self.gallery, self._gallery_token,
            )
            index = self.page - 1
            self._prev_style = self._gallery.pages[index - 1].style if index > 0 else ''
            self._next_style = self._gallery.pages[index + 1].style if index < self._gallery.pages_count - 1 else ''
            self.loaded = True


    @property
    def image(self):
        if not self.loaded:
            self.load()
        return self._image

    @property
    def prev(self):
        if not self.loaded:
            self.load()
        return self._prev

    @property
    def prev_style(self):
        if not self.loaded:
            self.load()
        return self._prev_style

    @property
    def next(self):
        if not self.loaded:
            self.load()
        return self._next

    @property
    def next_style(self):
        if not self.loaded:
            self.load()
        return self._next_style

    @property
    def pages(self):
        if not self.loaded:
            self.load()
        return self._gallery.pages_count

    @property
    def gallery_token(self):
        if not self.loaded:
            self.load()
        return self._gallery_token

    @classmethod
    def from_str(cls, s, *args, **kwargs):
        token, leftover = s.split('/')[-2:]
        gallery, page = leftover.split('-')
        return cls(*args, gallery=gallery, token=token, page=page, **kwargs)

    @classmethod
    def from_url(cls, url):
        response = http.get(url)

    @staticmethod
    def get_gallery_token(soup):
        return soup.get('href').split('/')[-2]
