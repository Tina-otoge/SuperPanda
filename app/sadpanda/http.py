import logging
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from flask import current_app, request

from app import store
from . import categories, pages

session = requests.session()
session.headers.update({'User-Agent': str(UserAgent().chrome)})
session.cookies.update({'sl': 'dm_2'})
session.cookies.update({'nw': '1'})
session.cookies.update({
    'ipb_member_id': store.get('member_id'),
    'ipb_pass_hash': store.get('pass_hash'),
    'sk': store.get('sk'),
})

methods = {
    'GET': session.get,
    'POST': session.post,
}

def build_url(url, base_url=None):
    base_url = base_url or (
        pages.SADPANDA_URL if store.get('sadpanda') else pages.EH_URL
    )
    if not url.startswith(('http://', 'https://')):
        url = urljoin(base_url, url)
    return url

def call(url: str, params={}, base_url=None, method='GET'):
    url = build_url(url, base_url=base_url)
    # logging.info('HTTP {} "{}" {}'.format(method, url, params))
    result = methods.get(method)(url, **params)
    if current_app.debug:
        with open('./output.html', 'wb') as f:
            f.write(result.content)
    return result

def encode_list(l):
    return ','.join(l)

def decode_list(s):
    if not s:
        return []
    return s.strip().split(',')

def get_filters(request_only=False):
    request_filters = request.args.getlist('filters')
    if request_only:
        return request_filters
    return (
        request_filters or
        decode_list(request.cookies.get('filters')) or
        ['non_h']
    )

def get_page():
    try:
        return int(request.args.get('page'))
    except TypeError:
        return 1

def to_soup(x):
    return BeautifulSoup(x, 'html.parser')
