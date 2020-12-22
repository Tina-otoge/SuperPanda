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
        data=Gallery.from_id(id, token, page=page),
    )

@main.route('/galleries/<int:id>-<string:token>/json')
def gallery_json(id, token):
    return jsonify(Gallery.from_id(id, token))

@main.route('/galleries/<int:id>-<string:token>/<int:page>')
def reader(id, token, page):
    gallery = Gallery.from_id(id, token, has_pages=[page])
    result = gallery.pages.get(page)
    result._gallery = gallery
    return render_template(
        'reader.html',
        data=result,
    )

@main.route('/galleries/<int:id>-<string:token>/<int:page>/json')
def reader_json(id, token, page):
    result = Gallery.from_id(id, token, has_pages=[page]).pages.get(page)
    result.load()
    return jsonify(result)
