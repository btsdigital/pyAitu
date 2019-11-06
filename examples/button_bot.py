import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Options, Form, Header, FormClosed, Button, FormAction

API_TOKEN = 'YOUR_API_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler()
async def send_ui(message: Message):

    # Header setting
    button_header = Header(
        _type="title",
        title="Button component",
        options=Options(
            closeable=True
        )
    )

    # Content setting
    button_content = Button(
        content_id="button_id",
        title="Custom button",
        button_type="default",
        options=Options(background_color="filled_dark"),
        form_action=FormAction(action="send_message", data_template="")
    )

    # Form setting
    form = Form(_id="form_id", header=button_header, content=button_content)

    # Form sending
    await bot.send_form(message.chat.id, form=form)


@dp.form_closed_handler()
async def get_form_closed(fc: FormClosed):
    await bot.send_message(fc.chat.id, "form is closed")


if __name__ == '__main__':
    executor.start_polling(dp)
