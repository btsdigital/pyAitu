from typing import List, Optional
from ..options import Options
from .content import Content
from ..validation_rule import ValidationRule
from .item import Item
from pyAitu.utils.serializer import serialized
from pyAitu.utils.dictionary_extractor import dictionary_of_object_if_exist


class RadioItem:
    def __init__(self, content_id: str, title: str):
        self.content_id = content_id
        self.title = title


class Radiogroup(Content):
    def __init__(
            self,
            content_id: str,
            title: Optional[str] = None,
            items: List[Item] = None,
            validations_rules: Optional[List[ValidationRule]] = None,
            options: Optional[Options] = None,
            default_value: Optional[Item] = None
    ):
        super().__init__(content_type="radiogroup", content_id=content_id)
        self.title = title
        self.items = serialized(items)
        self.validations_rules = serialized(validations_rules)
        self.options = dictionary_of_object_if_exist(options)
        self.default_value = serialized(default_value)
