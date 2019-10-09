from .content import Content
from ..options import Options
from ..validation_rule import ValidationRule
from typing import Dict, Optional, List

# Type alias
ValidationRules = List[ValidationRule]


def serialized(validation_rules: Optional[ValidationRules] = None) -> Optional[List[Dict[str, any]]]:
    if validation_rules is None:
        return None
    return list(map(lambda validation_rule: validation_rule.__dict__, validation_rules))


class Input(Content):
    def __init__(
            self,
            content_type: str,
            content_id: str,
            placeholder: Optional[str] = None,
            title: Optional[str] = None,
            mask: Optional[str] = None,
            text: Optional[str] = None,
            options: Optional[Options] = None,
            validation_rules: Optional[ValidationRules] = None,
    ):
        super().__init__(content_type, content_id)
        self.placeholder = placeholder
        self.title = title
        self.mask = mask
        self.text = text
        self.options = options.__dict__
        self.validations_rules = serialized(validation_rules)
