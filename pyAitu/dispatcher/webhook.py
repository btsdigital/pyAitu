from aiohttp import web
import asyncio
import asyncio.tasks
import datetime
import functools
import logging
import itertools
import typing
import json

from ..models import Update
from ..utils import helper

DEFAULT_WEB_PATH = '/webhook'
DEFAULT_ROUTE_NAME = 'webhook_handler'
BOT_DISPATCHER_KEY = 'BOT_DISPATCHER'

RESPONSE_TIMEOUT = 55

WEBHOOK = 'webhook'
WEBHOOK_CONNECTION = 'WEBHOOK_CONNECTION'
WEBHOOK_REQUEST = 'WEBHOOK_REQUEST'


log = logging.getLogger(__name__)


class PyAituWarning(Warning):
    pass


class TimeoutWarning(PyAituWarning):
    pass


class WebhookRequestHandler(web.View):
    """
        Simple Wehhook request handler for aiohttp web server.

        You need to register that in app:

        .. code-block:: python3

            app.router.add_route('*', '/your/webhook/path', WebhookRequestHandler, name='webhook_handler')

        But first you need to configure application for getting Dispatcher instance from request handler!
        It must always be with key 'BOT_DISPATCHER'

        .. code-block:: python3

            bot = Bot(TOKEN, loop)
            dp = Dispatcher(bot)
            app['BOT_DISPATCHER'] = dp

        """

    def get_dispatcher(self):
        """
        Get Dispatcher instance from environment

        :return: :class:`aiogram.Dispatcher`
        """
        return self.request.app[BOT_DISPATCHER_KEY]

    async def parse_update(self, bot):
        """
        Read update from stream and deserialize it.

        :param bot: bot instance. You an get it from Dispatcher
        :return: :class:`aiogram.types.Update`
        """
        data = await self.request.json()
        update = Update(**data)
        return update

    async def post(self):
        """
        Process POST request

        if one of handler returns instance of :class:`aiogram.dispatcher.webhook.BaseResponse` return it to webhook.
        Otherwise do nothing (return 'ok')

        :return: :class:`aiohttp.web.Response`
        """
        dispatcher = self.get_dispatcher()
        update = await self.parse_update(dispatcher.bot)

        results = await self.process_update(update)
        response = self.get_response(results)

        if response:
            web_response = response.get_web_response()
        else:
            web_response = web.Response(text='ok')

        if self.request.app.get('RETRY_AFTER', None):
            web_response.headers['Retry-After'] = self.request.app['RETRY_AFTER']

        return web_response

    async def get(self):
        return web.Response(text='')

    async def head(self):
        return web.Response(text='')

    async def process_update(self, update):
        """
        Need respond in less than 60 seconds in to webhook.

        So... If you respond greater than 55 seconds webhook automatically respond 'ok'
        and execute callback response via simple HTTP request.

        :param update:
        :return:
        """
        dispatcher = self.get_dispatcher()
        loop = dispatcher.loop or asyncio.get_event_loop()

        # Analog of `asyncio.wait_for` but without cancelling task
        waiter = loop.create_future()
        timeout_handle = loop.call_later(RESPONSE_TIMEOUT, asyncio.tasks._release_waiter, waiter)
        cb = functools.partial(asyncio.tasks._release_waiter, waiter)

        fut = asyncio.ensure_future(dispatcher.updates_handler.notify(update), loop=loop)
        fut.add_done_callback(cb)

        try:
            try:
                await waiter
            except asyncio.CancelledError:
                fut.remove_done_callback(cb)
                fut.cancel()
                raise

            if fut.done():
                return fut.result()
            else:
                # context.set_value(WEBHOOK_CONNECTION, False)
                fut.remove_done_callback(cb)
                fut.add_done_callback(self.respond_via_request)
        finally:
            timeout_handle.cancel()

    def respond_via_request(self, task):
        """
        Handle response after 55 second.

        :param task:
        :return:
        """
        log.warning(f"Detected slow response into webhook. "
             f"(Greater than {RESPONSE_TIMEOUT} seconds)\n"
             f"Recommended to use 'async_task' decorator from Dispatcher for handler with long timeouts.",
             TimeoutWarning)

        dispatcher = self.get_dispatcher()
        loop = dispatcher.loop or asyncio.get_event_loop()

        try:
            results = task.result()
        except Exception as e:
            loop.create_task(
                dispatcher.errors_handlers.notify(dispatcher, Update.get_current(), e))
        else:
            response = self.get_response(results)
            if response is not None:
                asyncio.ensure_future(response.execute_response(dispatcher.bot), loop=loop)

    def get_response(self, results):
        """
        Get response object from results.

        :param results: list
        :return:
        """
        if results is None:
            return None
        for result in itertools.chain.from_iterable(results):
            if isinstance(result, BaseResponse):
                return result


class BaseResponse:
    """
    Base class for webhook responses.
    """

    @property
    def method(self) -> str:
        """
        In all subclasses of that class you need to override this property

        :return: str
        """
        raise NotImplementedError

    def prepare(self) -> typing.Dict:
        """
        You need to override this method.

        :return: response parameters dict
        """
        raise NotImplementedError

    def cleanup(self) -> typing.Dict:
        """
        Cleanup response after preparing. Remove empty fields.

        :return: response parameters dict
        """
        return {k: v for k, v in self.prepare().items() if v is not None}

    def get_response(self):
        """
        Get response object

        :return:
        """
        return {'method': self.method, **self.cleanup()}

    def get_web_response(self):
        """
        Get prepared web response with JSON data.

        :return: :class:`aiohttp.web.Response`
        """
        return web.json_response(self.get_response(), dumps=json.dumps)

    async def execute_response(self, bot):
        """
        Use this method if you want to execute response as simple HTTP request.

        :param bot: Bot instance.
        :return:
        """
        method_name = helper.HelperMode.apply(self.method, helper.HelperMode.snake_case)
        method = getattr(bot, method_name, None)
        if method:
            return await method(**self.cleanup())
        return await bot.request(self.method, self.cleanup())

    async def __call__(self, bot=None):
        return await self.execute_response(bot)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self()