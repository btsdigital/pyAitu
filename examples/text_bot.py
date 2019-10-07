import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Options, Form, Header, FormClosed
from pyAitu.models.form.content.text import Text

API_TOKEN = 'YOUR_API_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler()
async def send_ui(message: Message):
    header_options = Options(
        closeable=True
    )
    text_options = Options(
        text_size="H1",
        text_style="bold",
        text_color="#000000",
    )
    header = Header(
        _type="toolbar",
        title="Title",
        options=header_options
    )
    text = Text(
        content_id="testid",
        content_type="text",
        title="Text test title ksdfgj sogijdhgdfgoh sdofghosu dfhgos dhfgojsdh fgodhsf gosdhfgopdhsfg sdfg",
        options=text_options
    )
    form = Form(_id="lol", header=header, content=text)
    await bot.send_form(message.chat.id, form=form)


@dp.form_closed_handler()
async def get_form_closed(fc: FormClosed):
    await bot.send_message(fc.chat.id, "form closed")


if __name__ == '__main__':
    executor.start_polling(dp)
