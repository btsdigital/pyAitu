class Options:
    def __init__(
            self,
            option_type: str = None,
            title: str = None,
            closeable: bool = None
    ):
        self.title = title
        self.type = option_type
        self.closeable = closeable
