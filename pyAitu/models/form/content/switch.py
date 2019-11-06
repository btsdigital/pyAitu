from ..options import Options
from .content import Content


class Switch(Content):
    def __init__(self, content_id: str, title: str = None, default_state: bool = False, options: Options = None):
        super().__init__(content_type="switch", content_id=content_id)
        self.title = title
        self.default_state = default_state
        if options is not None:
            self.options = options.__dict__
