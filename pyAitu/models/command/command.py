from .uiState import UiState
from .form_message import FormMessage
from ..peer import Recipient
from ..form import Form
from ...utils.strings import UI_STATE, RECIPIENT, TYPE, CONTENT, INLINE_COMMANDS


class Command:
    def __init__(self, peer_id, inline_commands: list = None):
        self.recipient = Recipient(peer_id)
        self.media = []
        self.inline_commands = []

        if inline_commands:
            for command in inline_commands:
                self.inline_commands.append(command.to_dict())

    def create_command(
            self,
            _type: str,
            media=None,
            content: str = "",
            reply_keyboard: list = None,
            quick_button_commands: list = None,
            form: Form = None
    ):
        commands = []
        form_message = FormMessage(form).__dict__ if form is not None else {}
        ui_state = UiState(
            reply_keyboard=reply_keyboard,
            quick_button_commands=quick_button_commands,
            form_message=form_message
        )

        body = {
            TYPE: _type,
            RECIPIENT: self.recipient.get_recipient(),
            CONTENT: content,
            UI_STATE: ui_state.to_dict(),
            INLINE_COMMANDS: self.inline_commands
        }

        if media:
            media_list = [media]
            body['mediaList'] = media_list

        commands.append(self.remove_none(body))

        return commands

    def remove_none(self, command: dict):
        return {k: v for k, v in command.items() if v is not None}
