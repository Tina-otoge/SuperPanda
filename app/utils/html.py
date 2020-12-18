from bs4 import BeautifulSoup

def get_gallery_page():
    with open('test_data/response.html') as f:
        return BeautifulSoup(f.read(), 'html.parser')
