import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Options, Form, Header, FormClosed, LabeledText, Indent

API_TOKEN = 'YOUR_API_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler()
async def send_ui(message: Message):
    header = Header(
        _type="toolbar",
        title="Title",
        options=Options(
            closeable=True
        )
    )
    text = LabeledText(
        content_id="testid",
        label="Some short title for label",
        title="Label text. It has fixed decoration and formatting, cannot change it with options",
        options=Options(
            indent_inner=Indent(
                right=5,
                top=5,
                bottom=10
            )
        )
    )
    form = Form(_id="lol", header=header, content=text, options=Options(fullscreen=True))
    await bot.send_form(message.chat.id, form=form)


@dp.form_closed_handler()
async def get_form_closed(fc: FormClosed):
    await bot.send_message(fc.chat.id, "form closed")


if __name__ == '__main__':
    executor.start_polling(dp)
