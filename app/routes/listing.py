from flask import jsonify, make_response, render_template

from app import main
from app.sadpanda import http, pages
from app.sadpanda.categories import FILTERS
from app.sadpanda.models import Gallery

@main.route('/galleries/')
def galleries(url=pages.GALLERIES_SEARCH_ROUTE, filters=None, title=None, *args, **kwargs):
    filters = http.get_filters() if filters is None else filters
    page = http.get_page()
    response = make_response(render_template(
        'galleries.html',
        title=title or 'Galleries',
        page=page,
        data=Gallery.get_galleries(url=url, page=page, filters=filters),
        filters_list=FILTERS,
        filters=filters,
        **kwargs,
    ))
    request_filters = http.get_filters(request_only=True)
    if request_filters:
        response.set_cookie('filters', http.encode_list(request_filters))
    return response

@main.route('/galleries/json')
def galleries_json():
    return jsonify(Gallery.get_galleries())

@main.route('/watched')
def watched():
    return galleries(
        title='Watched',
        url=pages.WATCHED_SEARCH_ROUTE,
        filters=[],
        route='.watched',
    )

@main.route('/popular')
def popular():
    return galleries(
        title='What\'s hot',
        url=pages.POPULAR_SEARCH_ROUTE,
        route='.popular',
    )

@main.route('/favorites')
def favorites():
    return galleries(
        title='Your favs',
        url=pages.FAVORITES_SEARCH_ROUTE,
        route='.favorites',
    )
