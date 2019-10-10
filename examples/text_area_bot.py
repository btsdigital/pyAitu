import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Options, Form, Header, FormClosed, \
    FormSubmitted, TextArea, Submit, FormAction, ValidationRule

API_TOKEN = 'YOUR_API_TOKEN'

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


def make_form() -> Form:
    form_id = "text_area_form_id"
    header = Header(_type="title", title="Text area component", options=Options(closeable=True))
    text_area = TextArea(
        content_id="text_area_id",
        content_type="text_area",
        title="Text Area",
        text="",
        placeholder="Enter your text here",
        validations_rules=[ValidationRule(type="required", value="true", error="You must fill this area")]
    )
    submit = Submit(
        content_id="submit_id",
        content_type="submit",
        title="Send",
        form_action=FormAction(action="submit_form", data_template="{"+form_id+".text_area_id}")
    )
    content = [text_area, submit]
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
