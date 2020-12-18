import json

from .json import default

def jdump(x, default=default, indent=2):
    print(json.dumps(x, default=default, indent=indent))
