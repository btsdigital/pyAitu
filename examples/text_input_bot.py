import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Item, Options, Form, Header, FormClosed, TextInput, ValidationRule

API_TOKEN = 'YOUR_API_TOKEN'

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
    text_input_content = TextInput(
        content_id="text_area_content_id",
        content_type="input",
        title="Cost",
        text="",
        placeholder="Enter your price",
        validations_rules=[ValidationRule(type="min", value="100000", error="Min. value is 100,000")],
        options=Options(input_type="money", currency="RUB"),
    )

    # Form setting
    form = Form(_id="form_id", header=text_input_header, content=text_input_content)

    # Form sending
    await bot.send_form(message.chat.id, form=form)


@dp.form_closed_handler()
async def get_form_closed(fc: FormClosed):
    await bot.send_message(fc.chat.id, "form is closed")


if __name__ == '__main__':
    executor.start_polling(dp)
