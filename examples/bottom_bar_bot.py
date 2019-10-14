import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Options, Form, Header, FormClosed, BottomBar, FormAction, FormSubmitted
import pyAitu.models.form.input_type as input_type
import pyAitu.models.form.currency as currency


API_TOKEN = 'YOUR_API_TOKEN'

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


def make_form() -> Form:
    form_id = "bottom_bar_form_id"
    header = Header(_type="title", title="Bottom bar component", options=Options(closeable=True))
    bottom_bar = BottomBar(
        content_type="bottom_bar",
        content_id="bottom_bar_id",
        title="Bottom Bar",
        form_action=FormAction(action="submit_form", data_template="Message from bottom bar")
    )
    return Form(_id=form_id, header=header, content=bottom_bar, options=Options(fullscreen=True))


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
