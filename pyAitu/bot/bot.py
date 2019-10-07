from typing import List, Dict, Optional
from ..models.peer import Recipient
from .base import BaseBot
from ..models import Update, Media, Command, QuickButtonCommand, InlineCommand, ReplyCommand, Form
from ..utils.strings import COMMANDS, SEND_MESSAGE, GET_UPDATES, UPLOADED_FILES, SEND_UI_STATE


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
                           ) -> Dict:

        command = Command(inline_commands=inline_commands)

        payload = {
            COMMANDS: command.create_command(
                SEND_MESSAGE,
                recipient=Recipient(peer_id),
                content=content,
                reply_keyboard=reply_keyboard,
                quick_button_commands=quick_button_commands
            )
        }

        result = await self.request(SEND_MESSAGE, payload)
        return result

    async def send_photo(self,
                         chat_id: str,
                         photo: str):
        result = await self.upload_file(photo)
        if result.get(UPLOADED_FILES):
            command = Command()
            media = Media(
                file_id=result.get(UPLOADED_FILES)[0]["fileId"],
                name=result.get(UPLOADED_FILES)[0]["fileName"],
                file_type="IMAGE"
            )

            payload = {
                COMMANDS: command.create_command(SEND_MESSAGE, recipient=Recipient(chat_id), media=media.to_dict())
            }
            result = await self.request(SEND_MESSAGE, payload)

            return result

    async def send_form(
            self,
            chat_id: str,
            form: Form
    ):
        command = Command()
        payload = {
            COMMANDS: command.create_command(SEND_UI_STATE, recipient=Recipient(chat_id), form=form)
        }

        result = await self.request(SEND_UI_STATE, payload)
        return result

    async def upload_file(self, file):
        files = {
            "file": file
        }

        return await self.request("UploadFile", None, files)

    async def send_ui_state(
            self,
            peer_id: str,
            quick_button_commands: List[QuickButtonCommand] = None,
            reply_keyboard: List[ReplyCommand] = None,
            show_camera_button=True,
            show_share_contact_button=True,
            show_record_audio_button=True,
            show_gallery_button=True,
            can_write_text=True
    ):
        command = Command()

        payload = {
            COMMANDS: command.create_command(
                _type=SEND_UI_STATE,
                recipient=Recipient(peer_id),
                quick_button_commands=quick_button_commands,
                reply_keyboard=reply_keyboard,
                show_camera_button=show_camera_button,
                show_share_contact_button=show_share_contact_button,
                show_record_audio_button=show_record_audio_button,
                show_gallery_button=show_gallery_button,
                can_write_text=can_write_text
            )
        }

        result = await self.request(SEND_UI_STATE, payload)
        return result
