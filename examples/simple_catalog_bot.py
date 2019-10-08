import logging
from pyAitu import executor, Bot, Dispatcher
from pyAitu.models import Message, SimpleCatalog, Item, Options, Form, Header, FormClosed, FormSubmitted, Submit, \
    FormAction, FormMessageSent

API_TOKEN = 'YOUR API TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['submit'])
async def send_submit_form(message: Message):
    form_options = Options(
        fullscreen=True
    )
    header_options = Options(
        closeable=True
    )
    header = Header(
        _type="toolbar",
        title="Title",
        options=header_options
    )
    form_action = FormAction(
        action="send_private_data",
        data_template="phone"
    )
    submit = Submit(
        content_id="lol",
        content_type="submit",
        form_action=form_action,
        title="отправь мой номер"
    )
    form = Form(_id="any id", header=header, content=submit, options=form_options)
    await bot.send_form(message.chat.id, form=form)


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


@dp.form_submitted_handler()
async def form_submitted_update(fs: FormSubmitted):
    await bot.send_message(fs.chat.id, fs.metadata)


@dp.form_message_sent_handler()
async def form_message_sent_update(fms: FormMessageSent):
    await bot.send_message(fms.chat.id, fms.message)

if __name__ == '__main__':
    executor.start_polling(dp)
