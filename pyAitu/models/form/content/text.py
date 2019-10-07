from pyAitu.models import Options
from pyAitu.models.form.content.content import Content


class Text(Content):
    def __init__(self, content_type: str, content_id, title: str, options: Options = None):
        super().__init__(content_type, content_id)
        self.options = options.__dict__
        self.title = title
