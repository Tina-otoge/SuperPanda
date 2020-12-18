class DictObject:
    def __init__(self, *args, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __repr__(self):
        return '<{}: {}>'.format(
            self.__class__.__name__,
            self.to_dict(),
        )

    def to_dict(self):
        return {k: getattr(self, k) for k in self.__dict__ if k[0] != '_'}

    def to_json(self):
        return self.to_dict()

