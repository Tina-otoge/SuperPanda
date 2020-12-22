from flask import jsonify, render_template

from app import main
from app.sadpanda import http, pages
from app.sadpanda.models import Gallery

@main.route('/galleries/<int:id>-<string:token>')
def gallery(id, token):
    page = http.get_page()
    return render_template(
        'gallery.html',
        title='Gallery',
        page=page,
        data=Gallery.get_gallery_from_id_token(id, token, page=page),
    )

@main.route('/galleries/<int:id>-<string:token>/json')
def gallery_json(id, token):
    return jsonify(Gallery.get_gallery_from_id_token(id, token))
