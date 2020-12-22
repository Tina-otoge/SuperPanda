import random

from . import main

@main.app_template_filter('nameify')
def nameify(x: str):
    return x.replace('_', ' ').capitalize()

@main.app_template_filter('refresh')
def refresh(x: str):
    return x + '?{}'.format(str(random.random())[2:8])

@main.app_template_filter('type')
def filter_type(o: object):
    return o.__class__.__name__
