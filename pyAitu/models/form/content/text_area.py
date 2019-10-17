from typing import List, Optional
from .content import Content
from ..options import Options
from ..validation_rule import ValidationRule
from pyAitu.utils.serializer import serialized
from pyAitu.utils.dictionary_extractor import dictionary_of_object_if_exist


class TextArea(Content):
    def __init__(
            self,
            content_id: str,
            title: Optional[str] = None,
            text: Optional[str] = None,
            placeholder: Optional[str] = None,
            validations_rules: Optional[List[ValidationRule]] = None,
            options: Optional[Options] = None
    ):
        super().__init__(content_type="text_area", content_id=content_id)
        self.title = title
        self.text = text
        self.validations_rules = serialized(validations_rules)
        self.placeholder = placeholder
        self.options = dictionary_of_object_if_exist(options)
