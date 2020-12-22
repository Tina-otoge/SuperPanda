import json

class Storage:
    def __init__(self, path=None, default={}, write_on_read=False, indent=4):
        self.data = default
        if path:
            with open(path) as f:
                self.data = json.load(f)
        self.path = path
        self.write_on_read = write_on_read
        self.json_args = {
            'indent': indent
        }

    def save(self):
        if not self.path:
            return
        with open(self.path, 'w') as f:
            json.dump(self.data, f, **self.json_args)

    def get(self, key, default=None):
        result = self.data.get(key, default)
        if self.write_on_read:
            self.set(key, result)
        return result

    def set(self, key, value):
        self.data[key] = value
        self.save()
