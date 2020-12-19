from flask import render_template

from . import main
from app.sadpanda.models import Page

@main.route('/reader/<int:gallery>/<int:page>-<string:token>')
def reader(gallery, page, token):
    return render_template(
        'reader.html',
        data=Page(gallery=gallery, page=page, token=token),
    )
