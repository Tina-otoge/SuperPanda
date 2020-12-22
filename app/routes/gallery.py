import logging
from flask import jsonify, redirect, render_template, url_for

from app import main
from app.sadpanda import http, pages
from app.sadpanda.models import Gallery

GALLERY_ID = '<int:id>-<string:token>'

@main.route('/galleries/{}'.format(GALLERY_ID))
def gallery(id, token):
    page = http.get_page()
    return render_template(
        'gallery.html',
        title='Gallery',
        page=page,
        data=Gallery.from_id(id, token, page=page),
    )

@main.route('/galleries/{}/json'.format(GALLERY_ID))
def gallery_json(id, token):
    return jsonify(Gallery.from_id(id, token))

@main.route('/galleries/{}/<int:page>'.format(GALLERY_ID))
def reader(id, token, page):
    gallery = Gallery.from_id(id, token, has_pages=[page])
    result = gallery.pages.get(page)
    result._gallery = gallery
    return render_template(
        'reader.html',
        data=result,
    )

@main.route('/galleries/{}/<int:page>/json'.format(GALLERY_ID))
def reader_json(id, token, page):
    result = Gallery.from_id(id, token, has_pages=[page]).pages.get(page)
    result.load()
    return jsonify(result)

@main.route('/favorites/{}/add'.format(GALLERY_ID))
def favorite_add(id, token):
    target = pages.GALLERY_ACTION_ROUTE.format(
        gallery=id, token=token, action='addfav',
    )
    result = http.call(target, method='POST', params={
        'favcat': 1,
        'apply': True,
        'update': 1,
    })
    return redirect(url_for('.gallery', id=id, token=token))

@main.route('/favorites/{}/delete'.format(GALLERY_ID))
def favorite_delete(id, token):
    target = pages.GALLERY_ACTION_ROUTE.format(
        gallery=id, token=token, action='addfav',
    )
    result = http.call(target, method='POST', params={
        'favcat': 'favdel',
        'apply': True,
        'update': 1,
    })
    return redirect(url_for('.gallery', id=id, token=token))
