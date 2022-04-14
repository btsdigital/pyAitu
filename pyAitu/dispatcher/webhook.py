from aiohttp import web
import logging
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

    async def parse_updates(self):
        """
        Read updates from stream and deserialize it.
        """
        data = await self.request.json()
        updates = []

        for jsonUpdate in data['updates']:
            update = Update(jsonUpdate)
            updates.append(update)

        return updates

    async def post(self):
        """
        Process POST request

        if one of handler returns instance of :class:`aiogram.dispatcher.webhook.BaseResponse` return it to webhook.
        Otherwise do nothing (return 'ok')

        :return: :class:`aiohttp.web.Response`
        """
        updates = await self.parse_updates()
        for update in updates:
            dispatcher = self.get_dispatcher()
            await dispatcher.updates_handler.notify(update)

        return web.Response(text='{"updates":[]}', content_type='application/json')

    async def get(self):
        return web.Response(text='')

    async def head(self):
        return web.Response(text='')



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