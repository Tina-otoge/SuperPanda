from app import eh


def get_page(id, page, page_token):
    soup = eh.get(f"/s/{page_token}/{id}-{page}")
    img = soup.find(id="img")
    return img["src"]
