from ..options import Options
from .content import Content
from pyAitu.models.form.form_action import FormAction
from pyAitu.utils.dictionary_extractor import extract_dictionary_if_exist_from


class Text(Content):
    def __init__(self, content_id, title: str, content_type: str = "text", options: Options = None, form_action: FormAction = None):
        super().__init__(content_type, content_id)
        self.title = title
        self.form_action = extract_dictionary_if_exist_from(form_action)

        if options is not None:
            self.options = options.__dict__
