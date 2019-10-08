from .form_update import FormUpdate


class FormMessageSent(FormUpdate):
    def __init__(self, json_object):
        super().__init__(json_object)
        self.message = json_object.get("message")
        self.message_id = json_object.get("messageId")
        self.additional_metadata = json_object.get("additionalMetadata")
