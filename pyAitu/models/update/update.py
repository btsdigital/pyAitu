from .message import Message
from .message_id_assigned import MessageIdAssigned
from .quick_button_selected import QuickButtonSelected
from .inline_command_selected import InlineCommandSelected
from .form_closed import FormClosed
from .form_submitted import FormSubmitted
from .form_message_sent import FormMessageSent


class Update:

    message: Message = None
    quick_button_selected: QuickButtonSelected = None
    inline_command_selected: InlineCommandSelected = None
    form_closed: FormClosed = None
    form_submitted: FormSubmitted = None
    form_message_sent: FormMessageSent = None
    message_id_assigned: MessageIdAssigned = None

    def __init__(self, json_object):
        self.updateId = json_object.get("updateId")
        self.updateType = json_object.get("type")

        if self.updateType == "Message":
            self.message = Message(json_object)
        if self.updateType == "QuickButtonSelected":
            self.quick_button_selected = QuickButtonSelected(json_object)
        if self.updateType == "InlineCommandSelected":
            self.inline_command_selected = InlineCommandSelected(json_object)
        if self.updateType == "FormMessageSent":
            self.form_message_sent = FormMessageSent(json_object)
        if self.updateType == "FormSubmitted":
            self.form_submitted = FormSubmitted(json_object)
        if self.updateType == "FormClosed":
            self.form_closed = FormClosed(json_object)
        if self.updateType == "MessageIdAssigned":
            self.message_id_assigned = MessageIdAssigned(json_object)
