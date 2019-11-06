from typing import Optional
from ..constants import Currency, Alignment, Orientation, TextSize, TextStyle, OptionMediaType, InputType
from .indent import Indent
from .flex_options import FlexOptions
from ...utils.dictionary_extractor import dictionary_purified_from_none, dictionary_of_object_if_exist


class Options:
    def __init__(
            self,
            type: Optional[str] = None,
            alignment: Optional[Alignment] = None,
            background: Optional[str] = None,
            background_color: Optional[str] = None,
            choice_type: Optional[str] = None,
            closeable: Optional[bool] = None,
            columns_count: Optional[int] = None,
            currency: Optional[Currency] = None,
            divider_type: Optional[str] = None,
            flex_options: Optional[FlexOptions] = None,
            fullscreen: Optional[bool] = None,
            has_back_action: Optional[bool] = None,
            height: Optional[int] = None,
            indent_inner: Optional[Indent] = None,
            indent_outer: Optional[Indent] = None,
            input_type: Optional[InputType] = None,
            item_left_icon_resource: Optional[str] = None,
            item_right_icon_resource: Optional[str] = None,
            item_type: Optional[str] = None,
            max_count: Optional[int] = None,
            max_date: Optional[str] = None,
            max_length: Optional[int] = None,
            media_type: Optional[OptionMediaType] = None,
            min_date: Optional[str] = None,
            orientation: Optional[Orientation] = None,
            search_enabled: Optional[bool] = None,
            show_divider: Optional[bool] = None,
            shape: Optional[str] = None,
            should_open_editor: Optional[bool] = None,
            subtitle_lines_count: Optional[int] = None,
            text_color: Optional[str] = None,
            text_size: Optional[TextSize] = None,
            text_style: Optional[TextStyle] = None,
            title: Optional[str] = None,
            title_lines_count: Optional[int] = None,
            width: Optional[int] = None
    ):
        self.type = type
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
        # Clean None values up
        self.purify_none_attributes()

    # Removes all None attributes of self
    # Mutating function, with side effect
    def purify_none_attributes(self):
        options_dictionary = dictionary_of_object_if_exist(obj=self)
        if options_dictionary:
            self.__dict__ = dictionary_purified_from_none(options_dictionary)

