from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from flask import request
import json

from . import categories

session = requests.session()
session.headers.update({'User-Agent': str(UserAgent().chrome)})
session.cookies.update({'sl': 'dm_2'})
session.cookies.update({'nw': '1'})
session.cookies.update({
    'ipb_member_id': '',
    'ipb_pass_hash': '',
})

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
