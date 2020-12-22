import json

class Storage:
    def __init__(self, path=None, default={}):
        self.data = default
        if path:
            with open(path) as f:
                self.data = json.load(f)
        self.path = path

    def save(self):
        if not self.path:
            return
        with open(self.path, 'w') as f:
            json.dump(self.data, f)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()
