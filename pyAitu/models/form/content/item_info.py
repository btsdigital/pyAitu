from ..options import Options
from .content import Content
from .file_metadata import FileMetadata


class ItemInfo(Content):
    def __init__(
            self,
            content_id: str,
            title: str = None,
            subtitle: str = None,
            file_metadata: FileMetadata = None,
            options: Options = None
    ):
        super().__init__(content_type="item_info", content_id=content_id)
        self.title = title
        self.subtitle = subtitle
        if file_metadata is not None:
            self.file_metadata = file_metadata.__dict__
        if options is not None:
            self.options = options.__dict__
