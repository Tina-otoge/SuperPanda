from flask import url_for

from app.utils import DictObject
from .. import http, pages

class Page(DictObject):
    def __init__(self, gallery=None, token=None, gallery_token=None, page=None, style=None, thumb=None, load=False):
        self.gallery = gallery
        self.token = token
        self.page = page
        self.style = style or ''
        self.thumb = thumb
        self.loaded = False
        self._gallery = None
        self._gallery_token = gallery_token
        self._image = None

        self.type = 'background' if self.style else 'image'

        if load:
            self.load()

    def __repr__(self):
        return '<{0.__class__.__name__}: {1}>'.format(self, str(self))

    def __str__(self):
        return '{0.gallery}#{0.page}'.format(self)

    def to_json(self):
        result = super().to_json()
        if self.loaded:
            result.update({
                'prev': str(self.prev),
                'next': str(self.next),
                'image': self.image,
                'gallery_token': self.gallery_token,
            })
        del result['loaded']
        result.update({
            'url': self.url,
        })
        return result

    @property
    def full_title(self):
        return 'Page #{0.page} of {0.extracted_title}'.format(self)

    @property
    def url(self):
        return pages.GALLERY_PAGE_ROUTE.format(
            token=self.token, gallery=self.gallery, page=self.page
        )

    @property
    def reader_url(self):
        return url_for(
            'main.reader',
            id=self.gallery,
            token=self.gallery_token,
            page=self.page
        )

    def load(self):
        if not self.loaded:
            from .gallery import Gallery
            soup = http.to_soup(http.call(self.url).content)
            self._gallery_token = self.get_gallery_token(
                soup.find('div', id='i5').find('a')
            )
            self._image = self.get_image(soup)
            if not getattr(self, '_gallery', False):
                self._gallery = Gallery.from_id(
                    self.gallery, self.gallery_token,
                    has_pages=self.get_needed_pages(self.page),
                )
            else:
                missing = [
                    x for x in self.get_needed_pages(self.page)
                    if x not in self._gallery.pages
                ]
                if missing:
                    self._gallery.pages.update(Gallery.from_id(
                        self.gallery, self.gallery_token, has_pages=missing
                    ).pages)
            self.loaded = True

    @property
    def gallery_token(self):
        if self._gallery_token:
            return self._gallery_token
        if self._gallery:
            return self._gallery.token
        return None


    @property
    def preloaded_image(self):
        if not self.loaded:
            self.load()
        if self._preloaded_image is None:
            soup = http.to_soup(http.call(self.next.url).content)
            self._preloaded_image = self.get_image(soup)
        return self._preloaded_image

    @property
    def pages(self):
        if not self.loaded:
            self.load()
        return self._gallery.pages

    @property
    def image(self):
        if not self.loaded:
            self.load()
        return self._image

    @property
    def prev(self):
        if not self.loaded:
            self.load()
        return self._gallery.pages.get(self.page - 1)

    @property
    def next(self):
        if not self.loaded:
            self.load()
        return self._gallery.pages.get(self.page + 1)

    @property
    def pages_count(self):
        if not self.loaded:
            self.load()
        return self._gallery.pages_count

    @property
    def tags(self):
        if not self.loaded:
            self.load()
        return self._gallery.tags

    @property
    def title(self):
        if not self.loaded:
            self.load()
        return self._gallery.title

    @property
    def extracted_title(self):
        if not self.loaded:
            self.load()
        return self._gallery.extracted_title

    @property
    def artist(self):
        if not self.loaded:
            self.load()
        return self._gallery.artist

    @classmethod
    def from_url_str(cls, s, *args, **kwargs):
        token, gallery, page = cls.get_ids_from_url(s)
        return cls(*args, gallery=gallery, token=token, page=page, **kwargs)

    @classmethod
    def from_link_with_img(cls, soup):
        token, gallery, page = cls.get_ids_from_url(soup.get('href'))
        return cls(
            gallery=gallery, token=token, page=page,
            thumb=soup.find('img').get('src')
        )


    @classmethod
    def from_gallery_id(cls, gallery_id, gallery_token, page, *args, **kwargs):
        gallery = Gallery.from_id(
            gallery_id, gallery_token,
            has_pages=cls.get_needed_pages(page),
        )
        return gallery.pages.get(page)

    @classmethod
    def from_url(cls, url):
        response = http.get(url)

    @staticmethod
    def get_needed_pages(index):
        if index == 1:
            return [index, index + 1]
        return [index - 1, index, index + 1]

    @staticmethod
    def get_gallery_token(soup):
        return soup.get('href').split('/')[-2]

    @staticmethod
    def get_image(soup):
        return soup.find('img', id='img').get('src')

    @staticmethod
    def get_ids_from_url(url):
        token, leftover = url.split('/')[-2:]
        gallery, page = leftover.split('-')
        return token, gallery, int(page)
