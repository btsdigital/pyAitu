import functools
from ..peer import Peer, PeerUser
from ..media import Image, Audio
from ...utils import helper


class Message:
    def __init__(self, json_object):
        self.updateId = json_object.get("updateId")
        self.messageId = json_object.get("messageId")
        self.dialog = Peer(json_object.get("dialog"))
        self.content = json_object.get("content")
        if json_object.get("author").get("type") == 'USER':
            self.author = PeerUser(json_object.get("author"))
        self.media = []

        if json_object.get("media"):
            for item in json_object.get("media"):
                if item.get("type") == "Image":
                    self.media.append(Image(item))
                elif item.get("type") == "Audio":
                    self.media.append(Audio(item))

    def is_command(self):
        return self.content and self.content.startswith('/')

    @property
    def chat(self):
        return self.dialog

    @property
    def text(self):
        return self.content

    @property
    @functools.lru_cache()
    def content_type(self):
        if self.media and self.media[0].type == "Image":
            return ContentType.PHOTO[0]
        elif self.media and self.media[0].type == "Audio":
            return ContentType.AUDIO[0]
        else:
            return ContentType.TEXT[0]


class ContentType(helper.Helper):
    mode = helper.HelperMode.snake_case

    TEXT = helper.ListItem()
    PHOTO = helper.ListItem()
    VIDEO = helper.ListItem()
    AUDIO = helper.ListItem()
    ANY = helper.ListItem()

