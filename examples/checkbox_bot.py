import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Options, Form, Header, FormClosed, ValidationRule, Submit, \
    FormAction
from pyAitu.models.form.content.checkbox import Checkbox
from pyAitu.models.constants.text_size import H1

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
    checkbox1 = Checkbox(
        content_id="checkbox1",
        title="Mark option 1",
        default_state=True
    )
    checkbox2 = Checkbox(
        content_id="checkbox2",
        title="Mark option 2",
        default_state=False,
        validations_rules=[ValidationRule(type="required", value="true", error="Поле не должно быть пустым")]
    )
    checkbox3 = Checkbox(
        content_id="checkbox3",
        title="Mark option 3",
        options=Options(
            text_size=H1,
            text_color="#FFEF00"
        )
    )
    submit = Submit(
        content_id="submit_id",
        title="Send",
        form_action=FormAction(
            action="submit_form"
        )
    )
    form = Form(
        _id="check_box_form",
        header=header,
        content=[checkbox1, checkbox2, checkbox3, submit],
        options=Options(fullscreen=True)
    )
    await bot.send_form(message.chat.id, form=form)


@dp.form_closed_handler()
async def get_form_closed(fc: FormClosed):
    await bot.send_message(fc.chat.id, "form closed")


if __name__ == '__main__':
    executor.start_polling(dp)
