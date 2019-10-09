import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Options, Form, Header, FormClosed, ValidationRule
from pyAitu.models.form.content import Input
import pyAitu.models.form.input_type as input_type
import pyAitu.models.form.currency as currency


API_TOKEN = '7e26eb35-2b45-46d5-8e1b-f79a4bfcccc4'

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dispatcher.message_handler()
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
    money_input_content = Input(
        content_id="input_money_content_id",
        content_type="input",
        title="Input Money",
        placeholder="Money input placeholder",
        validation_rules=[ValidationRule(type="min", value="10", error="Shoould be 10 minimum")],
        options=Options(input_type=input_type.MONEY, currency=currency.KZT)
    )

    double_input_content = Input(
        content_id="input_double_content_id",
        content_type="input",
        title="Input Double",
        placeholder="Double input placeholder",
        validation_rules=[ValidationRule(type="min", value="10", error="Shoould be 10 minimum")],
        options=Options(input_type=input_type.DOUBLE)
    )

    number_input_content = Input(
        content_id="input_number_content_id",
        content_type="input",
        title="Input Number",
        placeholder="Number input placeholder",
        options=Options(input_type=input_type.NUMBER)
    )

    text_input_content = Input(
        content_id="input_text_content_id",
        content_type="input",
        title="Input Text",
        placeholder="Text input placeholder",
        options=Options(input_type=input_type.TEXT),
        mask="[______]"
    )
    form_content = [money_input_content, double_input_content, number_input_content, text_input_content]
    # Form setting
    form = Form(_id="form_id", header=text_input_header, content=form_content)

    # Form sending
    await bot.send_form(message.chat.id, form=form)


@dispatcher.form_closed_handler()
async def get_form_closed(fc: FormClosed):
    await bot.send_message(fc.chat.id, "Form is closed")


if __name__ == '__main__':
    executor.start_polling(dispatcher)
