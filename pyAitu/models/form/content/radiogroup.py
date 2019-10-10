from typing import List, Optional
from ..options import Options
from .content import Content
from ..validation_rule import ValidationRule


class RadioItem:
    def __init__(self, content_id: str, title: str):
        self.content_id = content_id
        self.title = title


class Radiogroup(Content):
    def __init__(
            self,
            content_id: str,
            content_type: str,
            title: Optional[str] = None,
            items: [RadioItem] = None,
            validation_rules: Optional[List[ValidationRule]] = None,
            options: Optional[Optional] = None,
            default_value: Optional[RadioItem] = None
    ):
        self.content_id = content_id
        self.content_type = content_type
        self.title = title
        self.items = items
        self.validation_rules = validation_rules
        self.options = options
        self.default_value = default_value
