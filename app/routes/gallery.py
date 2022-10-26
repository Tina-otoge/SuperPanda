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

    def url(page):
        if page <= 0 or page > gallery.pages_count:
            return None
        return flask.url_for(
            "gallery_page",
            id=id,
            token=token,
            page=page,
            page_token=previews[page].page_token,
        )

    next_img = (
        eh.get_page(id, page + 1, previews[page + 1].page_token)
        if page < gallery.pages_count
        else None
    )

    pager = {
        "current": page,
        "total": gallery.pages_count,
        "first": url(1),
        "last": url(gallery.pages_count),
        "prev": url(page - 1),
        "next": url(page + 1),
    }
    return flask.render_template(
        "gallery_reader.html",
        gallery=gallery,
        previews=previews,
        img=img,
        pager=pager,
        next_img=next_img,
    )
