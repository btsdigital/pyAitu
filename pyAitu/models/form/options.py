from pyAitu.models.form.indent import Indent


class Options:
    def __init__(
            self,
            option_type: str = None,
            title: str = None,
            closeable: bool = None,
            text_size: str = None,
            text_style: str = None,
            text_color: str = None,
            fullscreen: bool = None,
            indent_inner: Indent = None,
            indent_outer: Indent = None,
    ):
        self.title = title
        self.type = option_type
        self.closeable = closeable
        self.text_size = text_size
        self.text_style = text_style
        self.text_color = text_color
        self.fullscreen = fullscreen
        if indent_inner is not None:
            self.indent_inner = indent_inner.__dict__
        if indent_outer is not None:
            self.indent_outer = indent_outer.__dict__
