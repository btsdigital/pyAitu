import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Options, Form, Header, FormClosed, ValidationRule, Submit, FormAction
from pyAitu.models.form.content.date_picker import DatePicker

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
    date_picker = DatePicker(
        content_id="date_id_1",
        title="Date title",
        selected_date="01-01-2019",
        options=Options(
            min_date="01-01-2018",
            max_date="01-01-2030"
        ),
        validations_rules=[ValidationRule(type="required", value="true", error="Это поле обязательно для заполнения")]
    )
    submit = Submit(
        content_id="submit_id",
        title="Send",
        form_action=FormAction(
            action="submit_form"
        )
    )
    form = Form(_id="date_picker_form", header=header, content=[date_picker, submit], options=Options(fullscreen=True))
    await bot.send_form(message.chat.id, form=form)


@dp.form_closed_handler()
async def get_form_closed(fc: FormClosed):
    await bot.send_message(fc.chat.id, "form closed")


if __name__ == '__main__':
    executor.start_polling(dp)
