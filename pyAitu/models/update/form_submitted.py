from .form_update import FormUpdate


class FormSubmitted(FormUpdate):
    def __init__(self, json_object):
        super().__init__(json_object)
        self.metadata = json_object.get("metadata")
        self.additional_metadata = json_object.get("additionalMetadata")
