from ..options import Options
from .content import Content


class Divider(Content):
    def __init__(self, content_id, content_type: str = "divider", options: Options = None):
        super().__init__(content_type, content_id)
        if options is not None:
            self.options = options.__dict__
