from ..peer import Peer


class QuickButtonSelected:
    def __init__(self, json_object):
        self.update_id = json_object.get("updateId")
        self.dialog = Peer(json_object.get("dialog"))
        self.sender = Peer(json_object.get("sender"))
        self.metadata = json_object.get("metadata")

    @property
    def from_user(self):
        return self.sender
