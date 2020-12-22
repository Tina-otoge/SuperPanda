from flask import redirect, url_for

from app import main
from . import gallery, listing, settings

@main.route('/')
def index():
    return redirect(url_for('.galleries'))
