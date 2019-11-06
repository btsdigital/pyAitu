from ...utils.strings import CAPTION


class ReplyCommand:
    def __init__(self, caption: str = None):
        self.caption = caption

    def to_dict(self):
        return {CAPTION: self.caption}
