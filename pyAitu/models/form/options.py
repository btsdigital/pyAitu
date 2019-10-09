from pyAitu.models.form.indent import Indent
from pyAitu.models.form.flex_options import FlexOptions


class Options:
    def __init__(
            self,
            alignment: str = None,
            background: str = None,
            background_color: str = None,
            choice_type: str = None,
            closeable: bool = None,
            columns_count: int = None,
            currency: str = None,
            divider_type: str = None,
            flex_options: FlexOptions = None,
            fullscreen: bool = None,
            has_back_action: bool = None,
            height: int = None,
            indent_inner: Indent = None,
            indent_outer: Indent = None,
            input_type: str = None,
            item_left_icon_resource: str = None,
            item_right_icon_resource: str = None,
            item_type: str = None,
            max_count: int = None,
            max_date: str = None,
            max_length: int = None,
            media_type: str = None,
            min_date: str = None,
            orientation: str = None,
            search_enabled: bool = None,
            show_divider: bool = None,
            shape: str = None,
            should_open_editor: bool = None,
            title: str = None,
            title_lines_count: int = None,
            subtitle_lines_count: int = None,
            text_size: str = None,
            text_style: str = None,
            text_color: str = None,
            width: int = None
    ):
        self.alignment = alignment
        self.background = background
        self.background_color = background_color
        self.choice_type = choice_type
        self.closeable = closeable
        self.columns_count = columns_count
        self.currency = currency
        self.divider_type = divider_type
        if flex_options is not None:
            self.flex_options = flex_options.__dict__
        self.fullscreen = fullscreen
        self.has_back_action = has_back_action
        self.height = height
        if indent_inner is not None:
            self.indent_inner = indent_inner.__dict__
        if indent_outer is not None:
            self.indent_outer = indent_outer.__dict__
        self.input_type = input_type
        self.item_left_icon_resource = item_left_icon_resource
        self.item_right_icon_resource = item_right_icon_resource
        self.item_type = item_type
        self.max_count = max_count
        self.max_date = max_date
        self.max_length = max_length
        self.media_type = media_type
        self.min_date = min_date
        self.orientation = orientation
        self.search_enabled = search_enabled
        self.show_divider = show_divider
        self.shape = shape
        self.should_open_editor = should_open_editor
        self.text_color = text_color
        self.title = title
        self.title_lines_count = title_lines_count
        self.subtitle_lines_count = subtitle_lines_count
        self.text_size = text_size
        self.text_style = text_style
        self.width = width
