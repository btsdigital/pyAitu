from typing import List, Optional
from ..options import Options
from .content import Content
from ..validation_rule import ValidationRule
from .item import Item
from pyAitu.utils.serializer import serialized
from pyAitu.utils.dictionary_extractor import dictionary_of_object_if_exist


class CustomContainer(Content):
    def __init__(
            self,
            content_id: str,
            content: List[Content],
            options: Optional[Options] = None

    ):
        super().__init__(content_type="custom_container", content_id=content_id)
        self.content = serialized(content)
        self.options = dictionary_of_object_if_exist(options)
