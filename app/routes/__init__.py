from flask import redirect, url_for

from app import main
from . import gallery

@main.route('/')
def index():
    return redirect(url_for('.gallery'))
