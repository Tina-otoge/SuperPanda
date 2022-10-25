import flask

from app import app, eh


@app.route("/galleries/")
def galleries():
    galleries = eh.get_galleries()
    return flask.render_template("galleries_list.html", galleries=galleries)


@app.route("/galleries/<int:id>-<token>/")
def gallery(id, token):
    gallery = eh.get_gallery(id, token)
    previews = eh.get_previews(id, token)
    return flask.render_template(
        "gallery_page.html", gallery=gallery, previews=previews
    )


@app.route("/galleries/<int:id>-<token>/<int:page>-<page_token>")
def gallery_page(id, token, page, page_token):
    gallery = eh.get_gallery(id, token)
    previews = eh.get_previews(id, token)
    img = eh.get_page(id, page, page_token)
    return flask.render_template(
        "gallery_reader.html", gallery=gallery, previews=previews, img=img
    )
