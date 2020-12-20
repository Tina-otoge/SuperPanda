from . import main

@main.app_template_filter('nameify')
def nameify(x: str):
    return x.replace('_', ' ').capitalize()
