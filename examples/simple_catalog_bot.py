import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, SimpleCatalog, Item, Options, Form, Header, FormClosed

API_TOKEN = '0efb7990-7d8b-4782-9919-8a254e768fc6'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler()
async def send_ui(message: Message):
    list_item = []
    item = Item(
        item_id="123",
        title="bro",
        subtitle="lol"
    )
    list_item.append(item)
    options = Options("list")
    header_options = Options(
        closeable=True
    )
    header = Header(
        _type="toolbar",
        title="Title",
        options=header_options
    )
    simple_catalog = SimpleCatalog(
        content_id="lol",
        content_type="simple_catalog",
        items=list_item,
        options=options
    )
    form = Form(_id="lol", header=header, content=simple_catalog)
    await bot.send_form(message.chat.id, form=form)


@dp.form_closed_handler()
async def get_form_closed(fc: FormClosed):
    await bot.send_message(fc.chat.id, "form closed")


if __name__ == '__main__':
    executor.start_polling(dp)
