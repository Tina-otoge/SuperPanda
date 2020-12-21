import json
from flask import jsonify, make_response, render_template

from app import main
from app.sadpanda import http
from app.sadpanda.categories import FILTERS
from app.sadpanda.models import Gallery

@main.route('/galleries/')
def galleries():
    filters = http.get_filters()
    page = http.get_page()
    response = make_response(render_template(
        'galleries.html',
        title='Galleries',
        data=Gallery.get_galleries(page=page),
        page=page,
        filters_list=FILTERS,
        filters=filters,
    ))
    request_filters = http.get_filters(request_only=True)
    if request_filters:
        response.set_cookie('filters', http.encode_list(request_filters))
    return response

@main.route('/galleries/json')
def galleries_json():
    return jsonify(Gallery.get_galleries())

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
