from .options import Options


class Header:
    def __init__(self, _type: str, title: str, options: Options = None):
        self.type = _type
        self.title = title
        self.options = options.__dict__ if options is not None else {}
