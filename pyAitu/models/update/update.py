from .message import Message
from .message_id_assigned import MessageIdAssigned
from .inline_command_selected import InlineCommandSelected


class Update:

    message: Message = None
    inline_command_selected: InlineCommandSelected = None
    message_id_assigned: MessageIdAssigned = None

    def __init__(self, json_object):
        self.updateId = json_object.get("updateId")
        self.updateType = json_object.get("type")

        if self.updateType == "Message":
            self.message = Message(json_object)
        if self.updateType == "InlineCommandSelected":
            self.inline_command_selected = InlineCommandSelected(json_object)
        if self.updateType == "MessageIdAssigned":
            self.message_id_assigned = MessageIdAssigned(json_object)
