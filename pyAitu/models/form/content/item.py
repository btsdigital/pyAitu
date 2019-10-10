from typing import List

from ..options import Options
from ..form_action import FormAction
from .file_metadata import FileMetadata
from .item_button import ItemButton


class Item:
    def __init__(
            self,
            item_id: str,
            title: str = None,
            subtitle: str = None,
            options: Options = None,
            form_action: FormAction = None,
            file_metadata: FileMetadata = None,
            item_buttons: List[ItemButton] = None
    ):
        self.id = item_id
        self.title = title
        self.subtitle = subtitle
        if options is not None:
            self.options = options.__dict__
        if form_action is not None:
            self.form_action = form_action.__dict__
        if file_metadata is not None:
            self.file_metadata = file_metadata.__dict__
        if item_buttons is not None:
            self.item_buttons = item_buttons
        self.__dict__ = self._remove_none()

    def _remove_none(self):
        return {k:v for k,v in self.__dict__.items() if v is not None}
