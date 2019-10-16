from ..peer import Peer


class MessageIdAssigned:
    def __init__(self, json_object):
        self.updateId = json_object.get("updateId")
        self.localId = json_object.get("localId")
        self.dialog = Peer(json_object.get("dialog"))
        self.id = json_object.get("id")

    @property
    def chat(self):
        return self.dialog
