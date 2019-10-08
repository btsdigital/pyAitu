from pyAitu.models.form.content.content import Content
from pyAitu.models.form.options import Options
from pyAitu.models.form.form_action import FormAction


class Button(Content):
    def __init__(
            self,
            content_id: str,
            content_type: str = "button",
            title: str = None,
            button_type: str = None,
            options: Options = None,
            form_action: FormAction = None
    ):
        super().__init__(content_type, content_id)
        self.title = title
        self.button_type = button_type
        self.options = options.__dict__
        self.form_action = form_action.__dict__
