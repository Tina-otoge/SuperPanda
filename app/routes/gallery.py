from flask import jsonify

from app import main
from app.sadpanda.models import Gallery

@main.route('/gallery')
def gallery():
    return jsonify(Gallery.get_galleries())
