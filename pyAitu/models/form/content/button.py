from pyAitu.models.form.options import Options
from pyAitu.models.form.form_action import FormAction


class Button:
    def __init__(
            self,
            id: str = None,
            type: str = None,
            title: str = None,
            button_type: str = None,
            options: Options = None,
            form_action: FormAction = None):
        self.id = id
        self.type = type
        self.title = title
        self.button_type = button_type
        self.options = options
        self.form_action = form_action
