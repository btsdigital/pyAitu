from ..peer import Peer


class InlineCommandSelected:
    def __init__(self, json_object):
        self.update_id = json_object.get("updateId")
        self.message_id = json_object.get("messageId")
        self.dialog = Peer(json_object.get("dialog"))
        self.sender = Peer(json_object.get("sender"))
        self.metadata = json_object.get("metadata")
        self.content = json_object.get("content")

    @property
    def from_user(self):
        return self.sender
