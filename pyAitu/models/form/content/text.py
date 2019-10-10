from ..options import Options
from .content import Content


class Text(Content):
    def __init__(self, content_id, title: str, options: Options = None):
        super().__init__(content_type="text", content_id=content_id)
        self.title = title
        if options is not None:
            self.options = options.__dict__
