import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Options, Form, Header, FormClosed, ValidationRule, Submit, FormAction, \
    FormSubmitted, Input
import pyAitu.models.constants.input_type as input_type
import pyAitu.models.constants.currency as currency


API_TOKEN = 'YOUR_API_TOKEN'

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


def make_form() -> Form:
    form_id = "input_form_id"
    header = Header(_type="title", title="Input component", options=Options(closeable=True))
    money_input = Input(
        content_id="input_money_id",
        title="Input Money",
        placeholder="Enter tenge here",
        options=Options(input_type=input_type.MONEY, currency=currency.KZT),
        validation_rules=[ValidationRule(type="required", value="true", error="This field is required")]
    )
    double_input = Input(
        content_id="input_double_id",
        title="Input Double",
        placeholder="Enter double value here",
        options=Options(input_type=input_type.DOUBLE),
        validation_rules=[ValidationRule(type="required", value="true", error="This field is required")]
    )
    number_input = Input(
        content_id="input_number_id",
        title="Input Number",
        placeholder="Enter decimal value here",
        options=Options(input_type=input_type.NUMBER),
        validation_rules=[ValidationRule(type="required", value="true", error="This field is required")]
    )
    text_input = Input(
        content_id="input_text_id",
        title="Input Text",
        placeholder="Enter text here",
        options=Options(input_type=input_type.TEXT),
        mask="[______]",
        validation_rules=[ValidationRule(type="required", value="true", error="This field is required")]
    )
    submit = Submit(
        content_id="submit_id",
        title="Send",
        form_action=FormAction(
            action="submit_form",
            data_template="Money: {%s.input_money_id},\nDouble: {%s.input_double_id}, \n" % (form_id, form_id) +
                          "Number: {%s.input_number_id},\nText: {%s.input_text_id}" % (form_id, form_id)
        )
    )
    content = [money_input, double_input, number_input, text_input, submit]
    return Form(_id=form_id, header=header, content=content)


@dispatcher.message_handler()
async def handle(message: Message):
    form = make_form()
    await bot.send_form(message.chat.id, form=form)


@dispatcher.form_submitted_handler()
async def handle_submission(submitted_form: FormSubmitted):
    await bot.send_message(
        submitted_form.chat.id,
        "Oh, it seems I have received text from you, look:\n" + f"{submitted_form.metadata}"
    )


@dispatcher.form_closed_handler()
async def handle_form_closing(closed_form: FormClosed):
    await bot.send_message(closed_form.chat.id, "Form is closed")


if __name__ == '__main__':
    executor.start_polling(dispatcher)
