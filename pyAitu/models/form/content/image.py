from .content import Content
from .file_metadata import FileMetadata
from ..options import Options
from ..form_action import FormAction


class Image(Content):
    def __init__(self,
                 content_type: str,
                 content_id: str,
                 file_metadata: FileMetadata,
                 photo_url: str = None,
                 options: Options = None,
                 form_action: FormAction = None):
        super().__init__(content_type, content_id)
        self.photo_url = photo_url
        self.file_metadata = file_metadata.__dict__
        self.options = options.__dict__ if options is not None else {}
        self.form_action = form_action.__dict__ if form_action is not None else None
