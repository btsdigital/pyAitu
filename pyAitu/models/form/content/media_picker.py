from typing import List, Optional

from .content import Content
from ..validation_rule import ValidationRule
from ..options import Options
from ....utils.serializer import serialized

ValidationRules = List[ValidationRule]


class MediaPicker(Content):
    def __init__(
            self,
            content_id: str,
            title: str,
            options: Optional[Options] = None,
            validations_rules: Optional[ValidationRules] = None,
    ):
        super().__init__(content_id=content_id, content_type="media_picker")
        self.title = title
        if options is not None:
            self.options = options.__dict__
        self.validations_rules = serialized(validations_rules)
