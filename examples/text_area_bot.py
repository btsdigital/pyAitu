import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Item, Options, Form, Header, FormClosed, TextArea, ValidationRule

API_TOKEN = '7e26eb35-2b45-46d5-8e1b-f79a4bfcccc4'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler()
async def send_ui(message: Message):

    # Header setting
    text_input_header = Header(
        _type="title",
        title="Input text component",
        options=Options(
            closeable=True
        )
    )

    # Content setting
    text_area = TextArea(
        content_id="text_area_content_id",
        content_type="input",
        title="Cost",
        text="",
        placeholder="Enter your price"
    )

    # Form setting
    form = Form(_id="form_id", header=text_input_header, content=text_area)

    # Form sending
    await bot.send_form(message.chat.id, form=form)


@dp.form_closed_handler()
async def get_form_closed(fc: FormClosed):
    await bot.send_message(fc.chat.id, "form is closed")


if __name__ == '__main__':
    executor.start_polling(dp)
