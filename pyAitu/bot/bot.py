from typing import List, Dict, Optional
from .base import BaseBot
from ..models import Update, Media, Command, QuickButtonCommand, InlineCommand, ReplyCommand, Form, Contact, CustomContainer
from ..utils.strings import COMMANDS, SEND_MESSAGE, GET_UPDATES, UPLOADED_FILES, SEND_UI_STATE, SEND_CONTACT_MESSAGE, \
    EDIT_MESSAGE, SEND_CONTAINER_MESSAGE
import json


class Bot(BaseBot):
    async def get_updates(self) -> List[Update]:
        result = await self.request(method=GET_UPDATES)
        return [Update(update) for update in result.get("updates", [])]

    async def send_message(self,
                           peer_id: str,
                           content: str,
                           quick_button_commands: List[QuickButtonCommand] = None,
                           inline_commands: List[InlineCommand] = None,
                           reply_keyboard: List[ReplyCommand] = None,
                           media_list: List[Media] = None,
                           local_id: str = None
                           ) -> Dict:
        command = Command(peer_id, inline_commands=inline_commands, media=media_list)

        payload = {
            COMMANDS: command.create_command(
                SEND_MESSAGE,
                content=content,
                reply_keyboard=reply_keyboard,
                quick_button_commands=quick_button_commands,
                local_id=local_id
            )
        }

        result = await self.request(SEND_MESSAGE, payload)
        return result

    async def edit_message(self,
                           peer_id: str,
                           message_id: str,
                           content: str,
                           inline_commands: List[InlineCommand] = None
                           ):
        command = Command(peer_id, inline_commands=inline_commands)

        payload = {
            COMMANDS: command.create_command(
                EDIT_MESSAGE,
                content=content,
                message_id=message_id
            )
        }

        result = await self.request(EDIT_MESSAGE, payload)
        return result

    async def send_photo(self,
                         chat_id: str,
                         photo: str):
        result = await self.upload_file(photo)
        if result.get(UPLOADED_FILES):
            media = Media(
                file_id=result.get(UPLOADED_FILES)[0]["fileId"],
                name=result.get(UPLOADED_FILES)[0]["fileName"],
                file_type="IMAGE"
            )
            command = Command(chat_id, media=[media])

            payload = {
                COMMANDS: command.create_command(SEND_MESSAGE)
            }
            result = await self.request(SEND_MESSAGE, payload)

            return result

    async def send_form(
            self,
            chat_id: str,
            form: Form
    ):
        command = Command(chat_id)
        payload = {
            COMMANDS: command.create_command(SEND_UI_STATE, form=form)
        }

        result = await self.request(SEND_UI_STATE, payload)
        return result

    async def send_container_message(
            self,
            chat_id: str,
            content: List
    ):

        dict_content = []

        for i in content:
            dict_content.append(i.__dict__)

        str_content = json.dumps(dict_content)

        command = Command(chat_id)
        payload = {
            COMMANDS: command.create_command(SEND_CONTAINER_MESSAGE, content=str_content)
        }

        result = await self.request(SEND_CONTAINER_MESSAGE, payload)
        return result

    async def upload_file(self, file):
        files = {
            "file": file
        }

        return await self.request("UploadFile", None, files)

    async def send_contact(
            self,
            chat_id: str,
            contact: Contact
    ):
        command = Command(chat_id)
        payload = {
            COMMANDS: command.create_command(SEND_CONTACT_MESSAGE, input_media=contact)
        }

        result = await self.request(SEND_UI_STATE, payload)
        return result
