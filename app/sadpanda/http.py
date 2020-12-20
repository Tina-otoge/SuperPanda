from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from flask import request
import json

from . import categories

session = requests.session()
session.headers.update({'User-Agent': str(UserAgent().chrome)})
session.cookies.update({'sl': 'dm_2'})
session.cookies.update({
    'ipb_member_id': '',
    'ipb_pass_hash': '',
})

def encode_list(l):
    return ','.join(l)

def decode_list(s):
    return s.split(',')

def get_filters():
    return (
        request.args.getlist('filters') or
        decode_list(request.cookies.get('filters')) or
        ['non-h']
    )

def to_soup(x):
    return BeautifulSoup(x, 'html.parser')
