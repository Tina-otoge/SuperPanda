import logging
import random
from flask import Flask, Blueprint, current_app
from flask_assets import Environment

from app.utils import LenientJSONEncoder, Storage

main = Blueprint('main', __name__)
store = Storage('./data.json')

@main.app_template_filter('refresh')
def refresh_filter(x):
    if not current_app.debug:
        return x
    return '{}?{}'.format(x, str(random.random())[2:8])

def create_app():
    app = Flask(__name__)
    app.json_encoder = LenientJSONEncoder
    app.register_blueprint(main)
    assets = Environment(app)
    logging.basicConfig(
        format='{levelname}: {message}',
        style='{',
        level=logging.DEBUG if app.debug else logging.WARNING,
    )
    return app

from . import routes, filters
