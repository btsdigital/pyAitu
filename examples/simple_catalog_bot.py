import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, SimpleCatalog, Item, Options, Form, Header, FormClosed, FormSubmitted, \
    FormMessageSent


API_TOKEN = 'YOUR_API_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler()
async def send_ui(message: Message):
    header = Header(_type="toolbar", title="Simple Catalog", options=Options(closeable=True))

    simple_catalog_items = []

    for i in range(20):
        simple_catalog_items.append(Item(item_id=f"item_id_{i}",
                                         title=f"item_title_{i}",
                                         subtitle=f"item_subtitle_{i}")
                                    )

    simple_catalog = SimpleCatalog(
        content_id="simple_catalog_id",
        items=simple_catalog_items,
        options=Options(type="list",
                        item_type="item_card",
                        columns_count=2,
                        show_divider=True,
                        item_right_icon_resource="ic_right_arrow")
    )

    form = Form(_id="form_id", header=header, content=simple_catalog)
    await bot.send_form(message.chat.id, form=form)


@dp.form_closed_handler()
async def get_form_closed(fc: FormClosed):
    await bot.send_message(fc.chat.id, "form closed")


@dp.form_submitted_handler()
async def form_submitted_update(fs: FormSubmitted):
    await bot.send_message(fs.chat.id, fs.metadata)


@dp.form_message_sent_handler()
async def form_message_sent_update(fms: FormMessageSent):
    await bot.send_message(fms.chat.id, fms.message)

if __name__ == '__main__':
    executor.start_polling(dp)
