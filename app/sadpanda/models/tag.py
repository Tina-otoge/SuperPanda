class Tag:
    namespace: str
    value: str

    def __repr__(self):
        return '<{0.__class__.__name__}: {1}>'.format(self, str(self))

    def __str__(self):
        return '{0.namespace}:{0.value}'.format(self)

    def to_json(self):
        return str(self)

    @classmethod
    def from_str(cls, s):
        result = cls()
        result.namespace, result.value = s.split(':') if s[0] != ':' else ('misc', s[1:])
        return result
