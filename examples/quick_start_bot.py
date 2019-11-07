"""
This is a echo bot
It echoes any incoming text messages
"""

import logging
from pyAitu import Bot, Dispatcher, executor
from pyAitu.models import Message

API_TOKEN = 'BOT_TOKEN_HERE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: Message):
    await bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    executor.start_polling(dp)