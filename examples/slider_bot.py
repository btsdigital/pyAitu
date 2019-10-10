import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, Options, Form, Header, FormClosed, Item
from pyAitu.models.form.content.file_metadata import FileMetadata
from pyAitu.models.form.content.slider import Slider
from pyAitu.utils.strings import UPLOADED_FILES

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
    file = await bot.upload_file("images/cat.jpg")
    items = []
    for i in range(3):
        items.append(
            Item(
                item_id="item" + str(i),
                file_metadata=FileMetadata(
                    file_id=file.get(UPLOADED_FILES)[0]["fileId"],
                    file_type="image",
                    file_name=file.get(UPLOADED_FILES)[0]["fileName"]
                )
            )
        )
    slider = Slider(
        content_id="slider",
        items=items
    )
    form = Form(_id="lol", header=header, content=slider)
    await bot.send_form(message.chat.id, form=form)


@dp.form_closed_handler()
async def get_form_closed(fc: FormClosed):
    await bot.send_message(fc.chat.id, "form closed")


if __name__ == '__main__':
    executor.start_polling(dp)
