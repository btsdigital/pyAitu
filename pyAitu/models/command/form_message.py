import json
from ..form import Form


class FormMessage:
    def __init__(self, json_form: Form):
        self.jsonForm = json.dumps(json_form.make_form())
