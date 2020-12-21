from flask import make_response, redirect, url_for

from .. import main

@main.route('/settings/theme/<string:name>')
def set_theme(name):
    response = make_response(redirect(url_for('.galleries')))
    response.set_cookie('theme', name)
    return response
