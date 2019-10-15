from .content import Content
from ..form_action import FormAction
from ..options import Options


class Submit(Content):
    def __init__(self,
                 content_id: str,
                 title: str,
                 form_action: FormAction,
                 options: Options = None):
        super().__init__(content_type="submit", content_id=content_id)
        self.title = title
        self.form_action = form_action.__dict__
        self.options = options.__dict__ if options is not None else {}
