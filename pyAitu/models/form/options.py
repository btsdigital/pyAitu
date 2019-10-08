from typing import Optional
from pyAitu.models.form import InputType
from pyAitu.models.form import Currency


class Options:
    def __init__(
            self,
            option_type: Optional[str] = None,
            title: Optional[str] = None,
            closeable: Optional[bool] = None,
            max_length: Optional[int] = None,
            input_type: Optional[InputType] = None,
            currency: Optional[Currency] = None,
    ):
        self.title = title
        self.type = option_type
        self.closeable = closeable
        self.max_length = max_length
        self.input_type = input_type
        self.currency = currency
