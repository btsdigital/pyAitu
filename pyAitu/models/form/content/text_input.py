from .content import Content
from ..options import Options
from ..validation_rules import ValidationRules
from pyAitu.utils.context import serialize_item


class TextInput(Content):
    def __init__(
            self,
            content_type: str,
            content_id,
            title: str,
            text: str,
            placeholder: str,
            validations_rules: [ValidationRules] = None,
            options: Options = None):

        super().__init__(content_type, content_id)
        self.title = title
        self.text = text
        self.validations_rules = serialize_item(items=validations_rules)
        self.placeholder = placeholder
        self.options = options.__dict__
