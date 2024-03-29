import logging
import os
from pyAitu import Bot, Dispatcher, executor
from pyAitu.models import Message, InlineCommandSelected, ContentType, \
     InlineCommand, Media, Contact, MessageIdAssigned
import pyAitu.models.constants.file_type as file_type

API_TOKEN = os.getenv("API_TOKEN", "YOU API TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


INLINE_COMMAND_MENU = [
    InlineCommand("1", "inline-command-data-ASD-1"),
    InlineCommand("2", "inline-command-data-ASD-2"),
    InlineCommand("3", "inline-command-data-ASD-3"),
]


@dp.message_handler(commands=['start', 'help'])
async def welcome(message: Message):
    await bot.send_message(message.chat.id, "Hello world")
    await bot.send_message(message.chat.id, "type keyboard")


@dp.message_handler(regexp='^cat$')
async def send_photo(message: Message):
    await bot.send_media(message.chat.id, 'images/cat.jpg', file_type.IMAGE)


@dp.message_handler(regexp='^sound$')
async def send_audio(message: Message):
    await bot.send_media(message.chat.id, 'audio/sample.mp3', file_type=file_type.AUDIO)


@dp.message_handler(regexp="^contact$")
async def send_contact(message: Message):
    await bot.send_contact(
        chat_id=message.chat.id,
        contact=Contact(
            first_name="contact_fname",
            last_name="contact_lname",
            phone_number="48884354864"
        )
    )


@dp.message_handler(regexp="^forward$")
async def forward_message(message: Message):
    await bot.forward_message(
        from_dialog=message.dialog.id,
        to_dialog=message.dialog.id,
        message_id=message.messageId
    )


@dp.message_handler(regexp="^webhook$")
async def send_webhook_info(message: Message):
    await bot.set_webhook("https://helloworld.com/path?q=query")
    webhook = await bot.get_webhook()
    await bot.send_message(message.chat.id, "you webhook is " + webhook.url)
    await bot.delete_webhook()


@dp.message_handler(regexp="^messageid$")
async def send_message(message: Message):
    await bot.send_message(message.chat.id, "New message for messageIdAssigned update", local_id="123456")


@dp.message_handler(regexp="^edit$")
async def send_message_for_edit(message: Message):
    await bot.send_message(message.chat.id, "This message will be edited", local_id="224421345")


@dp.message_id_assigned_handler(lambda message_id_assigned: message_id_assigned.localId == "224421345")
async def get_message_id(message_id_assigned: MessageIdAssigned):
    await bot.edit_message(
        peer_id=message_id_assigned.dialog.id,
        message_id=message_id_assigned.id,
        content="Now it is edited message"
    )


@dp.message_handler(commands=['media'])
async def send_media_message(message: Message):
    await bot.send_message(
        message.chat.id, "",
        media_list=[
            Media(
                file_id="your_video_id",
                file_type="VIDEO",
                name="lol"
            )
        ])


@dp.message_handler(content_types=ContentType.PHOTO)
async def get_photo(message: Message):
    await bot.download_file(message.media[0].fileId, destination='images/'+message.media[0].name)
    await bot.send_message(message.chat.id, "I got a photo")
    await bot.send_media(message.chat.id, 'images/' + message.media[0].name, file_type=file_type.IMAGE)


@dp.message_handler(content_types=ContentType.AUDIO)
async def get_photo(message: Message):
    await bot.download_file(message.media[0].fileId, destination='audio/'+message.media[0].name)
    await bot.send_message(message.chat.id, "I got an audio")
    await bot.send_media(message.chat.id, 'audio/' + message.media[0].name, file_type=file_type.AUDIO)


@dp.message_handler()
async def echo(message: Message):
    await bot.send_message(message.chat.id, message.text)


@dp.message_id_assigned_handler(lambda message_id_assigned: message_id_assigned.localId == "123456")
async def get_message_id(message_id_assigned: MessageIdAssigned):
    await bot.send_message(
        peer_id=message_id_assigned.dialog.id,
        content="got messageIdAssigned update with messageId " + message_id_assigned.id
    )


@dp.inline_command_handler(state="*", func=(lambda call: call.metadata.startswith('inline-command-data-')))
async def inline_menu_handler(ic: InlineCommandSelected):
    await bot.send_message(ic.dialog.id, "Got data from inline command: {}".format(ic.metadata))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
