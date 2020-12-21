import random
from flask import Flask, Blueprint, current_app
from flask_assets import Environment

from app.utils import LenientJSONEncoder

main = Blueprint('main', __name__)

def create_app():
    app = Flask(__name__)
    app.json_encoder = LenientJSONEncoder
    app.register_blueprint(main)
    assets = Environment(app)
    return app

from . import routes, filters
