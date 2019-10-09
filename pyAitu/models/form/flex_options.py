class FlexOptions:
    def __init__(
            self,
            flex_grow: float = None,
            flex_basis: float = None,
            flex_direction: str = None,
            flex_wrap: str = None,
            align_items: str = None,
            align_self: str = None,
            justify_content: str = None):
        self.flex_grow = flex_grow
        self.flex_basis = flex_basis
        self.flex_direction = flex_direction
        self.flex_wrap = flex_wrap
        self.align_items = align_items
        self.align_self = align_self
        self.justify_content = justify_content
