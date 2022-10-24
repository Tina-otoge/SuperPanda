import logging

from flask import Flask

app = Flask(__name__)

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

from . import routes
