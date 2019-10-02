from pyAitu.models.message import Message
from pyAitu.models.quick_button_selected import QuickButtonSelected
from pyAitu.models.inline_command_selected import InlineCommandSelected


class Update:

    message: Message = None
    quick_button_selected: QuickButtonSelected = None
    inline_command_selected: InlineCommandSelected = None

    def __init__(self, json_object):
        self.updateId = json_object.get("updateId")
        self.updateType = json_object.get("type")

        if self.updateType == "Message":
            self.message = Message(json_object)
        if self.updateType == "QuickButtonSelected":
            self.quick_button_selected = QuickButtonSelected(json_object)
        if self.updateType == "InlineCommandSelected":
            self.inline_command_selected = InlineCommandSelected(json_object)
