from ..options import Options
from .content import Content


class LabeledText(Content):
    def __init__(
            self,
            content_id: str,
            label: str,
            title: str,
            options: Options = None
    ):
        super().__init__(content_type="labeled_text", content_id=content_id)
        self.label = label
        self.title = title
        if options is not None:
            self.options = options.__dict__
