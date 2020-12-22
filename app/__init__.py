import logging
import random
from flask import Flask, Blueprint, current_app
from flask_assets import Environment
from flask_moment import Moment

from app.utils import LenientJSONEncoder, Storage

main = Blueprint('main', __name__)
store = Storage('./data.json', write_on_read=True)

def create_app():
    app = Flask(__name__)
    app.config['MOMENT_DEFAULT_FORMAT'] = 'LLL'
    app.config['SECRET_KEY'] = 'wow'
    app.json_encoder = LenientJSONEncoder
    app.register_blueprint(main)
    Environment(app)
    Moment(app)
    logging.basicConfig(
        format='{levelname}: {message}',
        style='{',
        level=logging.DEBUG if app.debug else logging.WARNING,
    )
    return app

from . import routes, filters
