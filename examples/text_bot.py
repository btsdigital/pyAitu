import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Options, Form, Header, FormClosed
from pyAitu.models.form.content.divider import Divider
from pyAitu.models.form.content.text import Text
from pyAitu.models.form.indent import Indent

API_TOKEN = 'YOUR_API_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler()
async def send_ui(message: Message):
    text_options = Options(
        text_size="H1",
        text_style="bold",
        text_color="#000000",
        indent_inner=Indent(
            right=5,
            top=5,
            bottom=10
        )
    )
    header = Header(
        _type="toolbar",
        title="Title",
        options=Options(
            closeable=True
        )
    )
    text1 = Text(
        content_id="testid",
        title="New test text for show before divider",
        options=text_options
    )
    text2 = Text(
        content_id="testid2",
        title="New test text for show after divider",
        options=text_options
    )
    divider = Divider(
        content_id="dividerid"
    )
    form = Form(_id="text_form", header=header, content=[text1, divider, text2], options=Options(fullscreen=True))
    await bot.send_form(message.chat.id, form=form)


@dp.form_closed_handler()
async def get_form_closed(fc: FormClosed):
    await bot.send_message(fc.chat.id, "form closed")


if __name__ == '__main__':
    executor.start_polling(dp)
