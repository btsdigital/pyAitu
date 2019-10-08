from .content import Content
from pyAitu.models.form import Options
from pyAitu.models.form import ValidationRule
from typing import Dict, Optional, List

# Type alias
ValidationRules = List[ValidationRule]


# Static function
def serialized(validation_rules: Optional[ValidationRules] = None) -> [Dict[str, any]]:
    return list(map(lambda validation_rule: validation_rule.__dict__, validation_rules))


class Input(Content):
    def __init__(
            self,
            content_type: str,
            content_id: str,
            placeholder: str = None,
            title: str = None,
            mask: str = None,
            text: str = None,
            options: Options = None,
            validation_rules: [ValidationRule] = None,
    ):
        super().__init__(content_type, content_id)
        self.placeholder = placeholder
        self.title = title
        self.mask = mask
        self.text = text
        self.options = options.__dict__
        self.validation_rules = serialized(validation_rules)
