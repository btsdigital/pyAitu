import json
from .uiState import UiState
from .recipient import Recipient
from ..utils.strings import UI_STATE, RECIPIENT, TYPE, CONTENT


class Command:
    def __init__(self, peer_id):
        self.recipient = Recipient(peer_id)
        self.ui_state = UiState()

    def create_command(self, _type: str, content):
        commands = []

        body = {
            TYPE: _type,
            RECIPIENT: self.recipient.get_recipient(),
            CONTENT: content,
            UI_STATE: self.ui_state.get_default_ui_state()
        }

        commands.append(body)

        return commands
