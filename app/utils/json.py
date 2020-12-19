import json

def default(x):
    if hasattr(x, 'to_json') and callable(x.to_json):
        return x.to_json()
    try:
        return json.JSONEncoder().default(x)
    except TypeError:
        return str(x)

class LenientJSONEncoder(json.JSONEncoder):
    def default(self, x):
        return default(x)
