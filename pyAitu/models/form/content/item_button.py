from ..form_action import FormAction


class ItemButton:
    def __init__(
            self,
            title: str,
            form_action: FormAction
    ):
        self.title = title
        self.form_action = form_action
