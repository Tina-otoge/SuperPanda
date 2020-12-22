import logging
import random
from flask import Flask, Blueprint, current_app
from flask_assets import Environment

from app.utils import LenientJSONEncoder, Storage

main = Blueprint('main', __name__)
store = Storage('./data.json')

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
