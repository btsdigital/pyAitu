from .content import Content
from ..options import Options
from ..validation_rule import ValidationRule
from typing import Optional, List
from pyAitu.utils.serializer import serialized
from pyAitu.utils.dictionary_extractor import dictionary_of_object_if_exist

# Type alias
ValidationRules = List[ValidationRule]


class Input(Content):
    def __init__(
            self,
            content_id: str,
            placeholder: Optional[str] = None,
            title: Optional[str] = None,
            mask: Optional[str] = None,
            text: Optional[str] = None,
            options: Optional[Options] = None,
            validation_rules: Optional[ValidationRules] = None,
    ):
        super().__init__(content_type="input", content_id=content_id)
        self.placeholder = placeholder
        self.title = title
        self.mask = mask
        self.text = text
        self.options = dictionary_of_object_if_exist(options)
        self.validations_rules = serialized(validation_rules)
