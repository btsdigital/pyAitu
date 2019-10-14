from .content import Content
from ..form_action import FormAction
from pyAitu.utils.dictionary_extractor import extract_dictionary_if_exist_from


class BottomBar(Content):

    def __init__(self, content_type: str, content_id: str, title: str, form_action: FormAction):
        super().__init__(content_type, content_id)
        self.title = title
        self.form_action = extract_dictionary_if_exist_from(form_action)
