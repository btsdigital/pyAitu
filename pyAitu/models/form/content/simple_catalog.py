from .content import Content
from ..options import Options


class SimpleCatalog(Content):
    def __init__(self, content_id, items: list, options: Options = None):
        super().__init__(content_type="simple_catalog", content_id=content_id)
        self.options = options.__dict__
        self.items = self.serialize_items(items)

    def serialize_items(self, items: list):
        result = []
        for item in items:
            result.append(item.__dict__)
        return result
