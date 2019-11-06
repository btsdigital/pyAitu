import json
from ..form import Form


class FormMessage:
    def __init__(self, form: Form):
        self.jsonForm = json.dumps(form.make_dictionary())
