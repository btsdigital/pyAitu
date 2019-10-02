from ...utils.strings import DEFAULT_USER, TYPE, ID


class Recipient:
    def __init__(self, _id: str):
        self.default_user = DEFAULT_USER
        self._id = _id

    def get_recipient(self):
        return {
            TYPE: self.default_user,
            ID: self._id
        }
