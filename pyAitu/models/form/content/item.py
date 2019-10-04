from typing import List
from ..options import Options
from ..form_action import FormAction
from .file_metadata import FileMetadata
from .item_button import ItemButton


class Item:
    def __init__(
            self,
            item_id: str,
            photo_url: str = None,
            title: str = None,
            subtitle: str = None,
            options: Options = None,
            form_action: FormAction = None,
            file_metadata: FileMetadata = None,
            item_buttons: List[ItemButton] = None
    ):
        self.id = item_id
        self.photo_url = photo_url
        self.title = title
        self.subtitle = subtitle
        self.options = options
        self.form_action = form_action
        self.file_metadata = file_metadata
        self.item_buttons = item_buttons
