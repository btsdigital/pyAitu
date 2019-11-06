from .content import Content
from ..options import Options
from ..form_action import FormAction


class Button(Content):
    def __init__(
            self,
            content_id: str,
            title: str = None,
            button_type: str = None,
            options: Options = None,
            form_action: FormAction = None
    ):
        super().__init__(content_type="button", content_id=content_id)
        self.title = title
        self.button_type = button_type
        self.options = options.__dict__
        self.form_action = form_action.__dict__
