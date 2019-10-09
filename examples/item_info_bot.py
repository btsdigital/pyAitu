import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Options, Form, Header, FormClosed
from pyAitu.models.form.content.item_info import ItemInfo

API_TOKEN = 'YOUR_API_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler()
async def send_ui(message: Message):
    item_info = ItemInfo(
        content_id="item_info_id",
        title="Item info title",
        subtitle="Subtitle for item info",
        options=Options(
            title_lines_count=2,
            subtitle_lines_count=3
        )
    )
    header = Header(
        _type="toolbar",
        title="Title",
        options=Options(closeable=True)
    )
    form = Form(_id="lol", header=header, content=item_info, options=Options(fullscreen=True))
    await bot.send_form(message.chat.id, form=form)


@dp.form_closed_handler()
async def get_form_closed(fc: FormClosed):
    await bot.send_message(fc.chat.id, "form closed")


if __name__ == '__main__':
    executor.start_polling(dp)
