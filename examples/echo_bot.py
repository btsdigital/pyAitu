import logging
from pyAitu import Bot, Dispatcher, executor
from pyAitu.models import Message, QuickButtonSelected, InlineCommandSelected, ContentType,\
    QuickButtonCommand, InlineCommand, ReplyCommand, Media
from pyAitu.models.media.contact import Contact

API_TOKEN = 'YOUR_API_TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


WELCOME_MENUS = [
    QuickButtonCommand("inline", 'welcome-menu-inline'),
    QuickButtonCommand("reply", 'welcome-menu-reply'),
    QuickButtonCommand("quick", 'welcome-menu-quick'),
]

INLINE_COMMAND_MENU = [
    InlineCommand("1", "inline-command-data-ASD-1"),
    InlineCommand("2", "inline-command-data-ASD-2"),
    InlineCommand("3", "inline-command-data-ASD-3"),
]

REPLY_COMMAND_MENU = [
    ReplyCommand("1"),
    ReplyCommand("2"),
    ReplyCommand("3"),
]

QUICK_BUTTON_COMMAND_MENU = [
    QuickButtonCommand("1", 'quick-button-data-ASD-1'),
    QuickButtonCommand("2", 'quick-button-data-ASD-2'),
    QuickButtonCommand("3", 'quick-button-data-ASD-3'),
]


@dp.message_handler(commands=['start', 'help'])
async def welcome(message: Message):
    await bot.send_message(message.chat.id, "Hello world")
    await bot.send_message(message.chat.id, "type keyboard")


@dp.message_handler(regexp='(^keyboard$)')
async def send_menu(message: Message):
    await bot.send_message(message.chat.id, "Select button", quick_button_commands=WELCOME_MENUS)


@dp.message_handler(regexp='^cat$')
async def send_photo(message: Message):
    await bot.send_photo(message.chat.id, 'images/cat.jpg')


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
    await bot.send_photo(message.chat.id, 'images/'+message.media[0].name)


@dp.message_handler()
async def echo(message: Message):
    await bot.send_message(message.chat.id, message.text)


@dp.quick_button_handler(state="*", func=(lambda call: call.metadata.startswith('welcome-menu-')))
async def menu_handler(qb: QuickButtonSelected):
    text = 'You chose'
    if qb.metadata.endswith('inline'):
        text += ' inline buttons'
        await bot.send_message(qb.dialog.id, text, inline_commands=INLINE_COMMAND_MENU)
    if qb.metadata.endswith('reply'):
        text += ' reply buttons'
        await bot.send_message(qb.dialog.id, text, reply_keyboard=REPLY_COMMAND_MENU)
    if qb.metadata.endswith('quick'):
        text += ' quick buttons'
        await bot.send_message(qb.dialog.id, text, quick_button_commands=QUICK_BUTTON_COMMAND_MENU)


@dp.inline_command_handler(state="*", func=(lambda call: call.metadata.startswith('inline-command-data-')))
async def inline_menu_handler(ic: InlineCommandSelected):
    await bot.send_message(ic.dialog.id, "Got data from inline command: {}".format(ic.metadata))


if __name__ == '__main__':
    executor.start_polling(dp)
