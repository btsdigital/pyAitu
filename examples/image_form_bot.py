import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Image, FileMetadata, Header, Form, Options

API_TOKEN = 'YOUR_API_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler()
async def send_image_form(message: Message):
    file_metadata = FileMetadata(
        file_type="image",
        file_id="YOUR IMAGE ID",
        file_name="YOUR IMAGE NAME"
    )
    image_options = Options(
        width=100,
        height=100
    )
    image = Image(
        content_id="pic",
        file_metadata=file_metadata,
        options=image_options
    )
    header = Header(
        _type="toolbar",
        title="Title"
    )
    form = Form(_id="lol", header=header, content=image)
    await bot.send_form(message.chat.id, form=form)

if __name__ == '__main__':
    executor.start_polling(dp)
