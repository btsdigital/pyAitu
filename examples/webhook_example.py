import logging
import os

from pyAitu import Bot, Dispatcher
from pyAitu.utils.executor import start_webhook

import pyAitu.models as models

API_TOKEN = os.getenv('API_TOKEN')

# webhook settings
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST', 'localhost:3001')
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 3001

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: models.Message):
    print("got message", message)
    # Regular request
    await bot.send_message(message.chat.id, message.text)


async def on_startup(dp):
    logging.info("on_startup")
    await bot.set_webhook(WEBHOOK_URL)
    result = await bot.get_webhook()
    logging.info(result.url)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )
