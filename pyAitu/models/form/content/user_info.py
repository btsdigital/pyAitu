from ..options import Options
from .content import Content


class UserInfo(Content):
    def __init__(
            self,
            content_id: str,
            user_id: str,
            options: Options = None
    ):
        super().__init__(content_type="user_info", content_id=content_id)
        self.user_id = user_id
        if options is not None:
            self.options = options
