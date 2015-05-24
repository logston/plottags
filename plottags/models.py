from .tag_parsers import TAG_STRING_PARSERS


class Tag:
    def __init__(self, tag_tuple):
        self.tag_str = tag_tuple[0]
        self.id = tag_tuple[1]
        self.dt = tag_tuple[2]
        self._value = None

    def __repr__(self):
        return '<Tag {}>'.format(self.tag_str)

    @property
    def value(self):
        if self._value is None:
            self._value = 0
            for tag_str_parser in TAG_STRING_PARSERS:
                value = tag_parser(self.tag_str)
                if value:
                    self._value = value
                    break
        return self._value

