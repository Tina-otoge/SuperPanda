from flask import jsonify, render_template

from app import main
from app.sadpanda.models import Gallery

@main.route('/galleries/')
def galleries():
    return render_template(
        'galleries.html',
        title='Galleries',
        data=Gallery.get_galleries(),
    )

@main.route('/galleries/json')
def galleries_json():
    return jsonify(Gallery.get_galleries())

@main.route('/galleries/<int:id>-<string:token>')
def gallery(id, token):
    return render_template(
        'gallery.html',
        title='Gallery',
        data=Gallery.get_gallery_from_id_token(id, token),
    )

@main.route('/galleries/<int:id>-<string:token>/json')
def gallery_json(id, token):
    return jsonify(Gallery.get_gallery_from_id_token(id, token))
