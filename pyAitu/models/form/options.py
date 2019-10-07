class Options:
    def __init__(
            self,
            option_type: str = None,
            title: str = None,
            closeable: bool = None,
            text_size: str = None,
            text_style: str = None,
            text_color: str = None
    ):
        self.title = title
        self.type = option_type
        self.closeable = closeable
        self.text_size = text_size
        self.text_style = text_style
        self.text_color = text_color
