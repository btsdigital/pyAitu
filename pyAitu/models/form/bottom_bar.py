from pyAitu.models.form.content.content import Content
from pyAitu.models.form.form_action import FormAction
from pyAitu.utils.dictionary_extractor import dictionary_of_object_if_exist


class BottomBar(Content):

    def __init__(self, content_id: str, title: str, form_action: FormAction):
        super().__init__("bottom_bar", content_id)
        self.title = title
        self.form_action = dictionary_of_object_if_exist(form_action)
