from .tag_parsers import TAG_TUPLE_STRING_PARSERS


class Tag:
    def __init__(self, tag_info):
        self.tag_str = tag_info[0]
        self.id = tag_info[1]
        self.dt = tag_info[2]
        self.tag_tuple = None
        for tag_str_parser in TAG_TUPLE_STRING_PARSERS:
            tup = tag_str_parser(self.tag_str)
            if tup is not None:
                self.tag_tuple = tup
                break
        
    def __repr__(self):
        return '<Tag {}>'.format(self.tag_str)


