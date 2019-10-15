from typing import List, Optional

from ..options import Options
from pyAitu.utils.serializer import serialized
from ..validation_rule import ValidationRule
from .content import Content

ValidationRules = List[ValidationRule]


class DatePicker(Content):
    def __init__(
            self,
            content_id: str,
            validations_rules: Optional[ValidationRules] = None,
            title: Optional[str] = None,
            selected_date: Optional[str] = None,
            options: Optional[Options] = None
    ):
        super().__init__(content_type="date_picker", content_id=content_id)
        self.title = title
        self.selected_date = selected_date
        if options is not None:
            self.options = options.__dict__
        self.validations_rules = serialized(validations_rules)
