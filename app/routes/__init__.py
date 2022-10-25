import flask

from app import app


@app.route("/")
def index():
    target = flask.url_for("galleries")
    return flask.redirect(target)


from . import gallery as gallery
