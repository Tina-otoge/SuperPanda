import flask

from app import app

from . import gallery


@app.route("/")
def index():
    return flask.url_for("galleries")
