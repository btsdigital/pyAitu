from ..peer import Peer


class FormUpdate:
    def __init__(self, json_object):
        self.update_id = json_object.get("updateId")
        self.form_id = json_object.get("formId")
        self.dialog = Peer(json_object.get("dialog"))
        self.sender = Peer(json_object.get("sender"))

    @property
    def chat(self):
        return self.dialog
