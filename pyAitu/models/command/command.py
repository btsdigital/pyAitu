from typing import List
from ..peer import Recipient
from ..media import Media, Contact
from ...utils.strings import RECIPIENT, TYPE, CONTENT, INLINE_COMMANDS, MEDIA_LIST, INPUT_MEDIA, LOCAL_ID, \
MESSAGE_ID, FROM_DIALOG, TO_DIALOG, DIALOG, DELETE_MESSAGE, INLINE_COMMAND_ROWS


class Command:
    def __init__(self, inline_commands: list = None, inline_command_rows: list = None, media: List[Media] = None):
        self.media = []
        self.inline_commands = []
        self.inline_command_rows = []

        if inline_commands:
            for command in inline_commands:
                self.inline_commands.append(command.to_dict())

        if inline_command_rows:
            for row in inline_command_rows:
                row_list = []
                for command in row:
                    row_list.append(command.to_dict())
                self.inline_command_rows.append(row_list)

        if media:
            for item in media:
                self.media.append(item.to_dict())

    def create_command(
            self,
            _type: str,
            peer_id: str = None,
            content: str = "",
            input_media: Contact = None,
            local_id: str = None,
            message_id: str = None,
            from_dialog: str = None,
            to_dialog: str = None,
            dialog: str = None
    ):
        commands = []
        if input_media is not None:
            input_media = input_media.__dict__

        body = {
            TYPE: _type,
            RECIPIENT: Recipient(peer_id).get_recipient(),
            CONTENT: content,
            INLINE_COMMANDS: self.inline_commands,
            INLINE_COMMAND_ROWS: self.inline_command_rows,
            MEDIA_LIST: self.media,
            INPUT_MEDIA: input_media,
            LOCAL_ID: local_id,
            MESSAGE_ID: message_id,
            FROM_DIALOG: Recipient(from_dialog).get_recipient(),
            TO_DIALOG: Recipient(to_dialog).get_recipient(),
            DIALOG: Recipient(dialog).get_recipient() if dialog else None
         }

        commands.append(self.remove_none(body))

        return commands

    def remove_none(self, command: dict):
        if command.get(TYPE) == DELETE_MESSAGE:
            return {k: v for k, v in command.items() if k in [TYPE, DIALOG, MESSAGE_ID]}
        return {k: v for k, v in command.items() if v is not None or {} or ''}
