from .form_update import FormUpdate


class FormClosed(FormUpdate):
    def __init__(self, json_object):
        super().__init__(json_object)
