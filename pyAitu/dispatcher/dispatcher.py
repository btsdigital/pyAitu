import asyncio
import logging
from typing import Optional
from .storage import BaseStorage, DisabledStorage
from .handler import Handler
from .middlewares import MiddlewareManager
from .filters import generate_default_filters
from ..models import ContentType
from ..bot import Bot
from ..utils import context

log = logging.getLogger(__name__)

MODE = 'MODE'
LONG_POLLING = 'long-polling'
UPDATE_OBJECT = 'update_object'


class Dispatcher:
    def __init__(self, bot, loop=None, storage: Optional[BaseStorage] = None, run_tasks_by_default: bool = False):
        if loop is None:
            loop = bot.loop
        if storage is None:
            storage = DisabledStorage()
        self.bot: Bot = bot
        self.loop = loop
        self.storage = storage
        self._polling = False
        self.run_tasks_by_default = run_tasks_by_default
        self._close_waiter = loop.create_future()

        self.updates_handler = Handler(self, middleware_key='update')
        self.message_handlers = Handler(self, middleware_key='message')
        self.quick_button_handlers = Handler(self, middleware_key='quick_button')
        self.inline_command_handlers = Handler(self, middleware_key='inline_command')
        self.error_handlers = Handler(self, once=False, middleware_key='error')
        self.middleware = MiddlewareManager(self)

        self.updates_handler.register(self.process_update)

    async def start_polling(self):
        if self._polling:
            raise RuntimeError('Polling already started')

        log.info('Polling started')

        context.set_value(MODE, LONG_POLLING)
        context.set_value('dispatcher', self)
        context.set_value('bot', self.bot)

        self._polling = True

        try:
            while self._polling:
                try:
                    updates = await self.bot.get_updates()
                except:
                    log.exception('Cause exception while getting updates')
                    await asyncio.sleep(15)
                    continue

                if updates:
                    log.debug(f"Received {len(updates)} updates.")
                    self.loop.create_task(self._process_polling_updates(updates))
        finally:
            self._close_waiter.set_result(None)
            log.warning('Polling is stopped')

    async def _process_polling_updates(self, updates):
        await self.process_updates(updates)

    async def process_updates(self, updates):
        tasks = []
        for update in updates:
            tasks.append(self.updates_handler.notify(update))
        return await asyncio.gather(*tasks)

    async def stop_polling(self):
        if self._polling:
            log.info('Stop polling...')
            self._polling = False

    def message_handler(self, *custom_filters, commands=None, content_types=None, state=None, run_task=None, **kwargs):
        def decorator(callback):
            self.register_message_handler(callback,
                                          commands=commands,
                                          content_types=content_types,
                                          custom_filters=custom_filters,
                                          state=state,
                                          run_task=run_task,
                                          **kwargs)
            return callback

        return decorator

    def register_message_handler(self,
                                 callback, *,
                                 commands=None,
                                 content_types=None,
                                 custom_filters=None,
                                 state=None,
                                 run_task=None,
                                 **kwargs):

        if content_types is None:
            content_types = ContentType.TEXT
        if custom_filters is None:
            custom_filters = []

        filters_set = generate_default_filters(self,
                                               *custom_filters,
                                               commands=commands,
                                               state=state,
                                               content_types=content_types,
                                               **kwargs)
        self.message_handlers.register(self._wrap_async_task(callback, run_task), filters_set)

    def quick_button_handler(self, *custom_filters, func=None, state=None, run_task=None, **kwargs):
        def decorator(callback):
            self.register_quick_button_handler(callback, func=func, state=state,
                                               custom_filters=custom_filters, run_task=run_task, **kwargs)
            return callback

        return decorator

    def register_quick_button_handler(self, callback, *, func=None,
                                      state=None, custom_filters=None, run_task=None, **kwargs):
        if custom_filters is None:
            custom_filters = []

        filters_set = generate_default_filters(self,
                                               *custom_filters,
                                               func=func,
                                               state=state,
                                               **kwargs)
        self.quick_button_handlers.register(self._wrap_async_task(callback, run_task), filters_set)

    def inline_command_handler(self, *custom_filters, func=None, state=None, run_task=None, **kwargs):
        def decorator(callback):
            self.register_inline_command_handler(callback, func=func, state=state,
                                                custom_filters=custom_filters, run_task=run_task, **kwargs)
            return callback
        return decorator

    def register_inline_command_handler(self, callback, *, func=None, state=None,
                                       custom_filters=None, run_task=None, **kwargs):
        if custom_filters is None:
            custom_filters = []
        filter_set = generate_default_filters(self,
                                              *custom_filters,
                                              func=func,
                                              state=state,
                                              **kwargs)
        self.inline_command_handlers.register(self._wrap_async_task(callback, run_task), filter_set)

    def _wrap_async_task(self, callback, run_task=None) -> callable:
        if run_task is None:
            run_task = self.run_tasks_by_default

        if run_task:
            return self.async_task(callback)
        return callback

    def async_task(self, callback):
        print('async task called')

    async def process_update(self, update):
        context.set_value(UPDATE_OBJECT, update)

        try:
            if update.message:
                state = await self.storage.get_state(chat=update.message.dialog.id,
                                                     user=update.message.author.id)
                context.update_state(chat=update.message.dialog.id,
                                     user=update.message.author.id,
                                     state=state)
                return await self.message_handlers.notify(update.message)
            if update.quick_button_selected:
                state = await self.storage.get_state(
                    chat=update.quick_button_selected.dialog.id if update.quick_button_selected else None,
                    user=update.quick_button_selected.sender.id
                )
                context.update_state(
                    user=update.quick_button_selected.sender.id,
                    state=state
                )
                return await self.quick_button_handlers.notify(update.quick_button_selected)
            if update.inline_command_selected:
                state = await self.storage.get_state(
                    chat=update.inline_command_selected.dialog.id if update.inline_command_selected else None,
                    user=update.inline_command_selected.sender.id
                )
                context.update_state(
                    user=update.inline_command_selected.sender.id,
                    state=state
                )
                return await self.inline_command_handlers.notify(update.inline_command_selected)
            else:
                print(update)
        except Exception as e:
            err = await self.error_handlers.notify(self, update, e)
            if err:
                return err
            raise
