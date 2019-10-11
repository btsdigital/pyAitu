import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Options, Form, Header, FormClosed, \
    FormSubmitted, Radiogroup, Submit, FormAction, ValidationRule, Item

API_TOKEN = 'YOUR_API_TOKEN'

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


def make_form() -> Form:
    form_id = "radiogroup_form_id"

    header = Header(_type="title", title="Radiogroup component", options=Options(closeable=True))

    radiogroup = Radiogroup(
        content_id="radiogroup",
        title="Radiogroup",
        options=Options(orientation="horizontal"),
        default_value=Item(item_id="radio_1", title="Default value"),
        items=[Item(item_id="radio_1", title="First"),
               Item(item_id="radio_2", title="Second")],
        validations_rules=[ValidationRule(type="required", value="true", error="Have to fill it!")]
    )

    submit = Submit(
        content_id="submit_id",
        content_type="submit",
        title="Send",
        form_action=FormAction(action="submit_form", data_template="{"+form_id+".radiogroup_id}")
    )

    content = [radiogroup, submit]

    return Form(_id=form_id, header=header, content=content)


@dispatcher.message_handler()
async def handle(message: Message):
    form = make_form()
    await bot.send_form(message.chat.id, form=form)


@dispatcher.form_submitted_handler()
async def handle_submission(submitted_form: FormSubmitted):
    await bot.send_message(
        submitted_form.chat.id,
        f"Oh, it seems I have received text from you, look:\n\"{submitted_form.metadata}\""
    )


@dispatcher.form_closed_handler()
async def handle_form_closing(closed_form: FormClosed):
    await bot.send_message(closed_form.chat.id, "Form is closed")


if __name__ == '__main__':
    executor.start_polling(dispatcher)
