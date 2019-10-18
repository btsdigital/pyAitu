import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Options, Form, Header, FormClosed, ValidationRule, Submit, FormAction, MediaPicker
from pyAitu.models.form.option_media_type import PHOTO, VIDEO

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
    image_picker = MediaPicker(
        content_id="image_picker1",
        title="Media image picker title",
        options=Options(
            media_type=PHOTO,
            height=10,
            width=80,
            max_count=1
        ),
        validations_rules=[ValidationRule(type="required", value="1", error="Выберите хотя бы 1 файл")]
    )
    video_picker = MediaPicker(
        content_id="video_picker1",
        title="Media video picker title",
        options=Options(
            should_open_editor=False,
            media_type=VIDEO,
            height=10,
            width=80,
            max_count=2
        ),
        validations_rules=[ValidationRule(type="required", value="1", error="Выберите хотя бы 1 файл")]
    )
    submit = Submit(
        content_id="submit_id",
        title="Send",
        form_action=FormAction(
            action="submit_form"
        )
    )
    form = Form(
        _id="media_picker_form",
        header=header,
        content=[image_picker, video_picker, submit],
        options=Options(fullscreen=True)
    )
    await bot.send_form(message.chat.id, form=form)


@dp.form_closed_handler()
async def get_form_closed(fc: FormClosed):
    await bot.send_message(fc.chat.id, "form closed")


if __name__ == '__main__':
    executor.start_polling(dp)
