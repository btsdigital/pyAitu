import asyncio
import secrets
import logging
import functools
import datetime

from uuid import UUID
from . import context
from typing import Callable, Union, Optional, Any
from ..dispatcher.webhook import BOT_DISPATCHER_KEY, DEFAULT_ROUTE_NAME
from aiohttp import web

APP_EXECUTOR_KEY = 'APP_EXECUTOR'

log = logging.getLogger('pyaitu')


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


def start_polling(dispatcher, *, loop=None, skip_updates=False, timeout=20, relax=0.1,
                  fast=True, on_startup=None, on_shutdown=None, reset_webhook=True):
    """
    Start bot in long-polling mode

    :param dispatcher:
    :param loop:
    :param skip_updates:
    :param reset_webhook:
    :param on_startup:
    :param on_shutdown:
    :param fast:
    :param timeout:
    """
    if not _check_token(dispatcher.bot.token):
        raise Exception('Token ' + dispatcher.bot.token + ' is not valid')

    executor = Executor(dispatcher, skip_updates=skip_updates, loop=loop)
    _setup_callbacks(executor, on_startup, on_shutdown)

    executor.start_polling(reset_webhook=reset_webhook, timeout=timeout, relax=relax, fast=fast)


def set_webhook(dispatcher, webhook_path: str, *, loop=None,
                skip_updates=False, on_startup=None,
                on_shutdown=None, retry_after: Optional[Union[str, int]],
                route_name= DEFAULT_ROUTE_NAME,
                web_app: None):

    executor = Executor(dispatcher, loop=loop, skip_updates=skip_updates)
    _setup_callbacks(executor, on_startup, on_shutdown)
    # executor.set_webhook(webhook_path, route_name=route_name, web_app=web_app)
    return executor


def start_webhook(dispatcher, webhook_path, *, loop=None, skip_updates=None,
                  on_startup=None, on_shutdown=None, retry_after=None, route_name=DEFAULT_ROUTE_NAME,
                  **kwargs):
    """
    Start bot in webhook mode

    :param dispatcher:
    :param webhook_path:
    :param loop:
    :param skip_updates:
    :param on_startup:
    :param on_shutdown:
    :param route_name:
    :param retry_after:
    :param kwargs:
    :return:
    """
    executor = set_webhook(dispatcher=dispatcher,
                           webhook_path=webhook_path,
                           loop=loop,
                           skip_updates=skip_updates,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           retry_after=retry_after,
                           route_name=route_name)
    executor.run_app(**kwargs)


def start(dispatcher, future, *, loop=None, skip_updates=None, on_startup=None, on_shutdown=None):
    """
    Execute Future.

    :param dispatcher: instance of Dispatcher
    :param future: future
    :param loop: instance of AbstractEventLoop
    :param skip_updates:
    :param on_startup:
    :param on_shutdown:
    :return:
    """
    executor = Executor(dispatcher, skip_updates=skip_updates, loop=loop)
    _setup_callbacks(executor, on_startup, on_shutdown)

    return executor.start(future)


class Executor:
    """
    Main executor class
    """

    def __init__(self, dispatcher, skip_updates=None, retry_after=None, loop=None):
        if loop is None:
            self._loop = loop

        self.dispatcher = dispatcher
        self.skip_updates = skip_updates
        self.retry_after = retry_after

        self._freeze = False

        self._identity = secrets.token_urlsafe(16)
        self._web_app = None

        self._on_startup_polling = []
        self._on_startup_webhook = []
        self._on_shutdown_polling = []
        self._on_shutdown_webhook = []

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return getattr(self, "_loop", asyncio.get_event_loop())

    @property
    def frozen(self):
        return self._freeze

    @property
    def web_app(self) -> web.Application:
        if self._web_app is None:
            raise RuntimeError('web.Application() is not configured!')
        return self._web_app

    def set_web_app(self, application: web.Application):
        """
        Change instance of aiohttp.web.Applicaton

        :param application:
        """
        self._web_app = application

    def on_startup(self, callback: callable, polling=True, webhook=False):
        """
        Register a callback for the startup process

        :param callback:
        :param polling: use with polling
        :param webhook: use with webhook
        """
        self._check_frozen()
        if not webhook and not polling:
            log.warning('This action has not effect!', UserWarning)
            return

        if isinstance(callback, (list, tuple, set)):
            for cb in callback:
                self.on_startup(cb, polling, webhook)
            return

        if polling:
            self._on_startup_polling.append(callback)
        if webhook:
            self._on_startup_webhook.append(callback)

    def on_shutdown(self, callback: callable, polling=True, webhook=False):
        """
        Register a callback for the shutdown process

        :param callback:
        :param polling: use with polling
        :param webhook: use with webhook
        """
        self._check_frozen()
        if not webhook and not polling:
            log.warning('This action has no effect!', UserWarning)
            return

        if isinstance(callback, (list, tuple, set)):
            for cb in callback:
                self.on_shutdown(cb, polling, webhook)
            return

        if polling:
            self._on_shutdown_polling.append(callback)
        if webhook:
            self._on_shutdown_webhook.append(callback)

    def _check_frozen(self):
        if self.frozen:
            raise RuntimeError('Executor is frozen')

    #
    # WebHook

    def _prepare_webhook(self, path=None, handler=None, route_name=DEFAULT_ROUTE_NAME, app=None):
        self._check_frozen()
        self._freeze = True

        if app is not None:
            self._web_app = app
        elif self._web_app is None:
            self._web_app = app = web.Application()
        else:
            raise RuntimeError("web.Application() is already configured!")

        if self.retry_after:
            app['RETRY_AFTER'] = self.retry_after

        if self._identity == app.get(self._identity):
            # App is already configured
            return

        if path is not None:
            app.router.add_route('*', path, handler, name=route_name)

        async def _wrap_callback(cb, _):
            return await cb(self.dispatcher)

        for callback in self._on_startup_webhook:
            app.on_startup.append(functools.partial(_wrap_callback, callback))

        async def _on_shutdown(_):
            await self._shutdown_webhook()

        app.on_shutdown.append(_on_shutdown)
        app[APP_EXECUTOR_KEY] = self
        app[BOT_DISPATCHER_KEY] = self.dispatcher
        app[self._identity] = datetime.datetime.now()

    def set_webhook(self, webhook_path=None, request_handler=None, route_name=DEFAULT_ROUTE_NAME, web_app=None):
        self._prepare_webhook(webhook_path, request_handler, route_name, web_app)
        self.loop.run_until_complete(self._startup_webhook())

    def run_app(self, **kwargs):
        web.run_app(self._web_app, **kwargs)

    def start_webhook(self, webhook_path=None, request_handler=None, route_name=DEFAULT_ROUTE_NAME, **kwargs):
        """
        Start bot in webhook mode

        :param webhook_path:
        :param request_handler:
        :param route_name: Name of webhook handler route
        :param kwargs:
        :return:
        """
        self.set_webhook(webhook_path=webhook_path, request_handler=request_handler, route_name=route_name)
        self.run_app(**kwargs)

    #
    # POLLING

    def _prepare_polling(self):
        self._check_frozen()
        self._freeze = True

        # self.loop.set_task_factory(context.task_factory)

    def start_polling(self, timeout=None, reset_webhook=None, relax=0.1, fast=True):
        """
        Start bot in long-polling mode

        :param reset_webhook:
        :param timeout:
        """
        self._prepare_polling()
        loop: asyncio.AbstractEventLoop = self.loop

        try:
            loop.run_until_complete(self._startup_polling())
            loop.create_task(self.dispatcher.start_polling(reset_webhook=reset_webhook,
                                                           timeout=timeout, relax=relax,
                                                           fast=fast))
            loop.run_forever()
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            loop.run_until_complete(self._shutdown_polling())
            log.warning("Goodbye!")

    def start(self, future):
        """
        Execute Future.

        Return the Future's result, or raise its exception.

        :param future:
        :return:
        """
        self._check_frozen()
        self._freeze = True
        loop: asyncio.AbstractEventLoop = self.loop

        try:
            loop.run_until_complete(self._startup_polling())
            result = loop.run_until_complete(future)
        except (KeyboardInterrupt, SystemExit):
            result = None
            loop.stop()
        finally:
            loop.run_until_complete(self._shutdown_polling())
            log.warning("Goodbye!")
        return result

    async def reset_webhook(self, check=True) -> bool:
        """
        Reset webhook

        :param check: check before deleting
        :return:
        """
        if check:
            wh = await self.dispatcher.bot.get_webhook_info()
            if not wh.url:
                return False

        return await self.dispatcher.bot.delete_webhook()

    async def _skip_updates(self):
        await self.dispatcher.reset_webhook(True)
        await self.dispatcher.skip_updates()
        log.warning(f"Updates were skipped successfully.")

    async def _startup_polling(self):
        if self.skip_updates:
            await self._skip_updates()
        for callback in self._on_startup_polling:
            await callback()

    async def _shutdown_polling(self):
        for callback in self._on_shutdown_polling:
            await callback()
        await self._shutdown()

    async def _startup_webhook(self):
        await self._welcome()
        if self.skip_updates:
            await self._skip_updates()

    async def _shutdown_webhook(self, wait_closed=False):
        for callback in self._on_shutdown_webhook:
            await callback(self.dispatcher)

        await self._shutdown()

        if wait_closed:
            await self.dispatcher.wait_closed()

    async def _shutdown(self):
        await self.dispatcher.stop_polling()

    async def _welcome(self):
        user = await self.dispatcher.bot.me
        log.info(f"Bot: {user.full_name} [@{user.username}]")

