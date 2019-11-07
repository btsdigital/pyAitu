===========
Quick start
===========

Simple template
---------------

At first you have to import all necessary modules

.. code-block:: python

    import logging
    from pyAitu import Bot, Dispatcher, executor
    from pyAitu.models import Message

Then you have to initialize bot and dispatcher instances. Bot token you can get from `@MasterService <https://i2.app.link/qoqX7m3d90>`_

.. code-block:: python

    API_TOKEN = 'BOT_TOKEN_HERE'

    #Configure logging
    logging.basicConfig(level=logging.INFO)

    #Initialize bot and dispatcher
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)

Next step: interaction with bot starts with **start** command. Register your first command handler:

.. code-block:: python

    @dp.message_handler(commands=['start'])
    async def send_welcome(message: Message)
    """
    This handler will be called when user sends `/start` command
    """
    await bot.send_message(message.chat.id, "Hello world!")

If you want to handle all messages in the chat simply add handler without filters

Last step: run long polling.

.. code-block:: python

    if __name__ == '__main__':
        executor.start_polling(dp)

Summary
-------

.. literalinclude:: ../../examples/quick_start_bot.py
    :language: python