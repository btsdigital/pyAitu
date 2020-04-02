from typing import List, Dict, Optional
from .base import BaseBot
from ..models import Update, Media, Command, QuickButtonCommand, InlineCommand, ReplyCommand, Form, Contact, \
    WebhookInfo, SetWebhook, FileType
from ..utils.strings import COMMANDS, SEND_MESSAGE, GET_UPDATES, UPLOADED_FILES, SEND_UI_STATE, SEND_CONTACT_MESSAGE, \
    EDIT_MESSAGE, SEND_CONTAINER_MESSAGE, FORWARD_MESSAGE, DELETE_MESSAGE
import json
import asyncio


class Bot(BaseBot):
    async def get_updates(self) -> List[Update]:
        result = await self.request(method=GET_UPDATES)
        for each in result.get("updates", []):
            if each.get("type") == "MessageIdAssigned":
                self.local_id_to_message_id[each.get("localId")] = each.get("id")
        return [Update(update) for update in result.get("updates", [])]

    async def send_message(self,
                           peer_id: str,
                           content: str,
                           quick_button_commands: List[QuickButtonCommand] = None,
                           inline_commands: List[InlineCommand] = None,
                           inline_command_rows: List[List[InlineCommand]] = None,
                           reply_keyboard: List[ReplyCommand] = None,
                           media_list: List[Media] = None,
                           local_id: str = None
                           ) -> Dict:
        command = Command(inline_commands=inline_commands, inline_command_rows=inline_command_rows, media=media_list)

        payload = {
            COMMANDS: command.create_command(
                SEND_MESSAGE,
                peer_id = peer_id,
                content=content,
                reply_keyboard=reply_keyboard,
                quick_button_commands=quick_button_commands,
                local_id=local_id
            )
        }

        result = await self.request(SEND_MESSAGE, payload)
        if local_id:
            while not self.local_id_to_message_id.get(local_id):
                await asyncio.sleep(0.5)
            return self.local_id_to_message_id.pop(local_id)
        return result

    async def forward_message(self,
                              from_dialog,
                              to_dialog: str,
                              message_id: str,
                              local_id: str = None
                              ):
        command = Command()

        payload = {
            COMMANDS: command.create_command(
                FORWARD_MESSAGE,
                from_dialog=from_dialog,
                to_dialog=to_dialog,
                message_id=message_id,
                local_id=local_id
            )
        }

        result = await self.request(SEND_MESSAGE, payload)
        return result

    async def edit_message(self,
                           peer_id: str,
                           message_id: str,
                           content: str,
                           inline_commands: List[InlineCommand] = None,
                           inline_command_rows: List[List[InlineCommand]] = None,
                           ):
        command = Command(inline_commands=inline_commands, inline_command_rows=inline_command_rows)

        payload = {
            COMMANDS: command.create_command(
                EDIT_MESSAGE,
                peer_id=peer_id,
                content=content,
                message_id=message_id
            )
        }

        result = await self.request(EDIT_MESSAGE, payload)
        return result

    async def send_media(self,
                         chat_id: str,
                         file: str,
                         file_type: FileType,
                         content: str = "",
                         local_id: str = None,
                         reply_keyboard: list = None):
        result = await self.upload_file(file)
        if result.get(UPLOADED_FILES):
            media = Media(
                file_id=result.get(UPLOADED_FILES)[0]["fileId"],
                name=result.get(UPLOADED_FILES)[0]["fileName"],
                file_type=file_type
            )
            command = Command(media=[media])

            payload = {
                COMMANDS: command.create_command(SEND_MESSAGE, chat_id, content, local_id=local_id,
                                                 reply_keyboard=reply_keyboard)
            }
            result = await self.request(SEND_MESSAGE, payload)
            if local_id:
                while not self.local_id_to_message_id.get(local_id):
                    await asyncio.sleep(0.5)
                return self.local_id_to_message_id.pop(local_id)
            return result

    async def send_media_by_id(self,
                               chat_id: str,
                               file_id: str,
                               file_type: FileType,
                               content: str = "",
                               local_id: str = None,
                               reply_keyboard: list = None):
        media = Media(
            file_id=file_id,
            name=file_id,
            file_type=file_type
        )
        command = Command(media=[media])

        payload = {
            COMMANDS: command.create_command(SEND_MESSAGE, chat_id, content, local_id=local_id,
                                             reply_keyboard=reply_keyboard)
        }
        result = await self.request(SEND_MESSAGE, payload)
        if local_id:
            while not self.local_id_to_message_id.get(local_id):
                await asyncio.sleep(0.5)
            return self.local_id_to_message_id.pop(local_id)
        return result

    async def send_form(
            self,
            chat_id: str,
            form: Form
    ):
        command = Command()
        payload = {
            COMMANDS: command.create_command(SEND_UI_STATE, chat_id, form=form)
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

        command = Command()
        payload = {
            COMMANDS: command.create_command(SEND_CONTAINER_MESSAGE, chat_id, content=str_content)
        }

        result = await self.request(SEND_CONTAINER_MESSAGE, payload)
        return result

    async def send_quick_button(
            self,
            chat_id: str,
            quick_button_commands: List[QuickButtonCommand] = None) -> Dict:

        command = Command()

        payload = {
            COMMANDS: command.create_command(
                SEND_UI_STATE,
                chat_id,
                quick_button_commands=quick_button_commands,
            )
        }

        result = await self.request(SEND_UI_STATE, payload)
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
        command = Command()
        payload = {
            COMMANDS: command.create_command(SEND_CONTACT_MESSAGE, chat_id, input_media=contact)
        }

        result = await self.request(SEND_UI_STATE, payload)
        return result
    
    async def delete_message(self, dialog: str, message_id: str):
        command = Command(inline_commands=None)

        payload = {
            COMMANDS: command.create_command(
                DELETE_MESSAGE,
                dialog=dialog,
                content=None,
                message_id=message_id
            )
        }
        result = await self.request(DELETE_MESSAGE, payload)
        return result

    async def edit_message_reply_markup(self, peer_id: str,
                                        message_id: str,
                                        inline_commands: List[InlineCommand] = None,
                                        inline_command_rows: List[List[InlineCommand]] = None):
        command = Command(inline_commands=inline_commands, inline_command_rows=inline_command_rows)

        payload = {
            COMMANDS: command.create_command(
                EDIT_MESSAGE,
                content=None,
                peer_id=peer_id,
                message_id=message_id
            )
        }

        result = await self.request(EDIT_MESSAGE, payload)
        return result

    async def get_webhook(self) -> WebhookInfo:
        result = await self.request("GetWebhook")
        return WebhookInfo(result)

    async def set_webhook(self, url: str):
        result = await self.request("SetWebhook", SetWebhook(url).__dict__)
        return result

    async def delete_webhook(self):
        return await self.request("DeleteWebhook")
