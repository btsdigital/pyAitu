from typing import List, Dict
from .base import BaseBot
from ..types import Update, Command, QuickButtonCommand, InlineCommand, ReplyCommand
from ..utils.strings import COMMANDS


class Bot(BaseBot):
    async def get_updates(self) -> List[Update]:
        result = await self.request(method="GetUpdates")
        return [Update(update) for update in result.get("updates", [])]

    async def send_message(self,
                           peer_id: str,
                           content: str,
                           quick_button_commands: List[QuickButtonCommand] = None,
                           inline_commands: List[InlineCommand] = None,
                           reply_keyboard: List[ReplyCommand] = None
                           ) -> Dict:

        command = Command(peer_id)

        payload = {
            COMMANDS: command.create_command("SendMessage", content)
        }

        if quick_button_commands is not None:
            keyboard = []
            for command in quick_button_commands:
                keyboard.append(command.to_dict())
            payload['commands'][0]['uiState']['quickButtonCommands'] = keyboard
        if inline_commands is not None:
            keyboard = []
            for command in inline_commands:
                keyboard.append(command.to_dict())
            payload['commands'][0]['inlineCommands'] = keyboard
        if reply_keyboard is not None:
            keyboard = []
            for command in reply_keyboard:
                keyboard.append(command.to_dict())
            payload['commands'][0]['uiState']['replyKeyboard'] = keyboard

        result = await self.request("SendMessage", payload)
        return result
