from typing import List, Optional
from .content import Content
from ..options import Options
from ..validation_rule import ValidationRule
from pyAitu.utils.serializer import serialized


class TextArea(Content):
    def __init__(
            self,
            content_type: str,
            content_id: str,
            title: Optional[str] = None,
            text: Optional[str] = None,
            placeholder: Optional[str] = None,
            validations_rules: [ValidationRule] = None,
            options: Optional[Options] = None):

        super().__init__(content_type, content_id)
        self.title = title
        self.text = text
        self.validations_rules = serialized(validations_rules)
        self.placeholder = placeholder
        self.options = options.__dict__
