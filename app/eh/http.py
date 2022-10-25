from datetime import timedelta

import requests_cache
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

BASE_URL = "https://e-hentai.org"
COOKIE_DISPLAY_MODE_NAME = "sl"
COOKIE_DISPLAY_MODE_EXTENDED = "dm_2"

session = requests_cache.CachedSession(
    "data/eh-http-cache", expire_after=timedelta(hours=2)
)
session.headers.update({"User-Agent": str(UserAgent().chrome)})
session.cookies.update({COOKIE_DISPLAY_MODE_NAME: COOKIE_DISPLAY_MODE_EXTENDED})
# session.proxies = {"https": "http://proxy_url:port"}


def get(url: str) -> BeautifulSoup:
    if url.startswith("/"):
        url = BASE_URL + url
    print('HTTP GET "{}"'.format(url))
    result = session.get(url)

    with open("output.html", "w") as f:
        f.write(result.text)

    result.raise_for_status()

    if len(result.text) == 0:
        raise Exception("Empty response")

    if result.text.startswith(
        "Your IP address has been temporarily banned for excessive pageloads"
    ):
        raise Exception("temp ban: {}".format(result.text))

    return BeautifulSoup(result.text, "html.parser")
