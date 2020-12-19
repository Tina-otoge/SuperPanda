from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

session = requests.session()
session.headers.update({'User-Agent': str(UserAgent().chrome)})
session.cookies.update({'sl': 'dm_2'})

def to_soup(x):
    return BeautifulSoup(x, 'html.parser')
