from flask import Flask, Blueprint

from app.utils import LenientJSONEncoder

main = Blueprint('main', __name__)

def create_app():
    app = Flask(__name__)
    app.json_encoder = LenientJSONEncoder
    app.register_blueprint(main)
    return app

from . import routes
