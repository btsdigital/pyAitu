from ...utils.strings import CAPTION, METADATA, ACTION


class QuickButtonCommand:
    def __init__(self, caption: str, metadata: str, action: str = 'QUICK_REQUEST'):
        self._caption = caption
        self._metadata = metadata
        self._action = action

    @property
    def caption(self):
        return self._caption

    @property
    def metadata(self):
        return self._metadata

    @property
    def action(self):
        return self._action

    def to_dict(self):
        return {
            CAPTION: self.caption,
            METADATA: self.metadata,
            ACTION: self.action
        }
