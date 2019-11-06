from ...utils.strings import CAPTION, METADATA


class InlineCommand:
    def __init__(self, caption: str, metadata: str):
        self._caption = caption
        self._metadata = metadata

    @property
    def caption(self):
        return self._caption

    @property
    def metadata(self):
        return self._metadata

    def to_dict(self):
        return {
            CAPTION: self.caption,
            METADATA: self.metadata
        }
