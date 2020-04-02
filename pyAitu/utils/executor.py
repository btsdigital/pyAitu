import asyncio
from uuid import UUID
import logging
from . import context


def _check_token(token: str) -> bool:
    try:
        UUID(token, version=4)
        return True
    except ValueError:
        return False


def _setup_callbacks(executor, on_startup=None, on_shutdown=None):
    if on_startup is not None:
        executor.on_startup(on_startup)
    if on_shutdown is not None:
        executor.on_shutdown(on_shutdown)


def start_polling(dispatcher, *, loop=None, skip_updates=False, timeout=None,
                  on_startup=None, on_shutdown=None):
    if not _check_token(dispatcher.bot.token):
        raise Exception('Token ' + dispatcher.bot.token + ' is not valid')
    executor = Executor(dispatcher, loop=loop)
    _setup_callbacks(executor, on_startup, on_shutdown)
    executor.start_polling(timeout=timeout)


class Executor:
    def __init__(self, dispatcher, skip_updates=None, loop=None):
        if loop is None:
            loop = dispatcher.loop
        self.loop = loop
        self.dispatcher = dispatcher
        self.skip_updates = skip_updates
        self._freeze = False

        self._on_startup_polling = []
        self._on_shutdown_polling = []

    @property
    def frozen(self):
        return self._freeze

    def on_startup(self, callback: callable, polling=True, webhook=False):
        logger = logging.getLogger('Executor(on_startup)')
        logger.info('on START')
        self._on_startup_polling.append(callback)

    def on_shutdown(self, callback: callable, polling=True, webhook=False):
        logger = logging.getLogger('Executor(on_shutdown)')
        logger.info('on SHUT')
        self._on_shutdown_polling.append(callback)

    def _check_frozen(self):
        if self.frozen:
            raise RuntimeError('Executor is frozen')

    def _prepare_polling(self):
        self._check_frozen()
        self._freeze = True

        self.loop.set_task_factory(context.task_factory)

    def start_polling(self, timeout=None):

        self._prepare_polling()
        loop: asyncio.AbstractEventLoop = self.loop

        try:
            loop.run_until_complete(self._startup_polling())
            loop.create_task(self.dispatcher.start_polling())
            loop.run_forever()
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            loop.run_until_complete(self._shutdown_polling())

    async def _skip_updates(self):
        print('skip updates')

    async def _startup_polling(self):
        if self.skip_updates:
            await self._skip_updates()
        for callback in self._on_startup_polling:
            await callback()

    async def _shutdown_polling(self):
        for callback in self._on_shutdown_polling:
            await callback()
        await self._shutdown()

    async def _shutdown(self):
        await self.dispatcher.stop_polling()
