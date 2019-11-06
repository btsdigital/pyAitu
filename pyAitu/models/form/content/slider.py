from ..options import Options
from .content import Content


class Slider(Content):
    def __init__(self, content_id: str, items: list, options: Options = None):
        super().__init__(content_type="slider", content_id=content_id)
        self.items = self.serialize_items(items)
        if options is not None:
            self.options = options.__dict__

    def serialize_items(self, items: list):
        result = []
        for item in items:
            result.append(item.__dict__)
        return result
