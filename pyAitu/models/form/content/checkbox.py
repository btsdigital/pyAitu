from typing import Optional, List

from ..options import Options
from ..validation_rule import ValidationRule
from .content import Content
from pyAitu.utils.serializer import serialized

ValidationRules = List[ValidationRule]


class Checkbox(Content):
    def __init__(
            self,
            content_id: str,
            title: str,
            default_state: bool = False,
            options: Optional[Options] = None,
            validations_rules: Optional[ValidationRules] = None,
    ):
        super().__init__(content_type="checkbox", content_id=content_id)
        self.title = title
        self.default_state = default_state
        if options is not None:
            self.options = options.__dict__
        if validations_rules is not None:
            self.validations_rules = serialized(validations_rules)
