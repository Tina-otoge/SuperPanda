class Tag:
    def __init__(self, namespace=None, value=None):
        self.namespace = namespace
        self.value = value

    def __repr__(self):
        return '<{0.__class__.__name__}: {1}>'.format(self, str(self))

    def __str__(self):
        return '{0.namespace}:{0.value}'.format(self)

    def to_json(self):
        return str(self)

    @classmethod
    def from_str(cls, s):
        if s[0] == ':':
            return cls('misc', s[1:])
        words = s.split(':')
        if len(words) < 2:
            value = words[0]
            namespace = 'misc'
        else:
            namespace, value = words
        return cls(namespace=namespace, value=value)

    @classmethod
    def language(cls, s):
        return cls('language', s.lower())
