from ..options import Options
from .content import Content
from pyAitu.models.form.form_action import FormAction
from pyAitu.utils.dictionary_extractor import dictionary_of_object_if_exist


class Text(Content):
    def __init__(self, content_id, title: str, options: Options = None, form_action: FormAction = None):
        super().__init__(content_type="text", content_id=content_id)
        self.title = title
        self.form_action = dictionary_of_object_if_exist(form_action)
        if options is not None:
            self.options = options.__dict__
