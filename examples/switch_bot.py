import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Options, Form, Header, FormClosed, Divider, Text, Indent
from pyAitu.models.form.content.switch import Switch

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
    switch1 = Switch(
        content_id="switch_id1",
        title="Вы согласны с условиями?"
    )
    switch2 = Switch(
        content_id="switch_id2",
        title="Вы точно согласны с условиями???",
        default_state=False
    )
    form = Form(_id="text_form", header=header, content=[switch1, switch2], options=Options(fullscreen=True))
    await bot.send_form(message.chat.id, form=form)


@dp.form_closed_handler()
async def get_form_closed(fc: FormClosed):
    await bot.send_message(fc.chat.id, "form closed")


if __name__ == '__main__':
    executor.start_polling(dp)
