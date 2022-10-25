import webassets
from webassets import Bundle, Environment

from app import app

environment = Environment(
    directory=app.static_folder,
    url=app.static_url_path,
)


environment.register(
    "css",
    Bundle(
        "scss/main.scss",
        depends="**/*.scss",
        filters=webassets.filter.get_filter(
            "libsass",
            includes=["app/lib/materialize/sass"],
        ),
        output="style.css",
    ),
)

environment.register(
    "js",
    Bundle(
        "js/main.js",
        filters="rjsmin",
        output="script.js",
    ),
)


@app.context_processor
def inject_assets():
    return {
        "assets": environment,
    }
