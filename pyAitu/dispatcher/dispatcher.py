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
        self.message_id_assigned_handlers = Handler(self, middleware_key='message_id_assigned')
        self.inline_command_handlers = Handler(self, middleware_key='inline_command')
        self.form_closed_handlers = Handler(self, middleware_key='form_closed')
        self.form_submitted_handlers = Handler(self, middleware_key='form_submitted')
        self.form_message_sent_handlers = Handler(self, middleware_key='form_message_sent')
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

    def message_id_assigned_handler(self, *custom_filters, func=None, state=None, run_task=None, **kwargs):
        def decorator(callback):
            self.register_message_id_assigned_handler(callback, func=func, state=state,
                                                      custom_filters=custom_filters, run_task=run_task, **kwargs)
            return callback

        return decorator

    def register_message_id_assigned_handler(self, callback, *, func=None,
                                             state=None, custom_filters=None, run_task=None, **kwargs):
        if custom_filters is None:
            custom_filters = []

        filters_set = generate_default_filters(self,
                                               *custom_filters,
                                               func=func,
                                               state=state,
                                               **kwargs)
        self.message_id_assigned_handlers.register(self._wrap_async_task(callback, run_task), filters_set)

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

    def form_closed_handler(self, *custom_filters, func=None, state=None, run_task=None, **kwargs):
        def decorator(callback):
            self.register_form_closed_handler(callback, *custom_filters, func=func,
                                              state=state, run_task=run_task, **kwargs)
            return callback

        return decorator

    def register_form_closed_handler(self, callback, *, func=None, state=None,
                                     custom_filters=None, run_task=None, **kwargs):
        if custom_filters is None:
            custom_filters = []
        filter_set = generate_default_filters(self,
                                              *custom_filters,
                                              func=func,
                                              state=state,
                                              **kwargs)
        self.form_closed_handlers.register(self._wrap_async_task(callback, run_task), filter_set)

    def form_submitted_handler(self, *custom_filters, func=None, state=None, run_task=None, **kwargs):
        def decorator(callback):
            self.register_form_submitted_handler(callback, *custom_filters, func=func,
                                                 state=state, run_task=run_task, **kwargs)
            return callback

        return decorator

    def register_form_submitted_handler(self, callback, *, func=None, state=None,
                                        custom_filters=None, run_task=None, **kwargs):
        if custom_filters is None:
            custom_filters = []
        filter_set = generate_default_filters(self,
                                              *custom_filters,
                                              func=func,
                                              state=state,
                                              **kwargs)
        self.form_submitted_handlers.register(self._wrap_async_task(callback, run_task), filter_set)

    def form_message_sent_handler(self, *custom_filters, func=None, state=None, run_task=None, **kwargs):
        def decorator(callback):
            self.register_form_message_sent_handler(callback, *custom_filters, func=func,
                                                    state=state, run_task=run_task, **kwargs)
            return callback

        return decorator

    def register_form_message_sent_handler(self, callback, *, func=None, state=None,
                                           custom_filters=None, run_task=None, **kwargs):
        if custom_filters is None:
            custom_filters = []
        filter_set = generate_default_filters(self,
                                              *custom_filters,
                                              func=func,
                                              state=state,
                                              **kwargs)
        self.form_message_sent_handlers.register(self._wrap_async_task(callback, run_task), filter_set)

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
                await self.state_updater(update.message)
                return await self.message_handlers.notify(update.message)
            elif update.quick_button_selected:
                await self.state_updater(update.quick_button_selected)
                return await self.quick_button_handlers.notify(update.quick_button_selected)
            elif update.inline_command_selected:
                await self.state_updater(update.inline_command_selected)
                return await self.inline_command_handlers.notify(update.inline_command_selected)
            elif update.form_closed:
                await self.state_updater(update.form_closed)
                return await self.form_closed_handlers.notify(update.form_closed)
            elif update.form_message_sent:
                await self.state_updater(update.form_message_sent)
                return await self.form_message_sent_handlers.notify(update.form_message_sent)
            elif update.form_submitted:
                await self.state_updater(update.form_submitted)
                return await self.form_submitted_handlers.notify(update.form_submitted)
            elif update.message_id_assigned:
                await self.state_updater(update.message_id_assigned)
                return await self.message_id_assigned_handlers.notify(update.message_id_assigned)
            else:
                print("Undefined update " + update.updateType)
        except Exception as e:
            err = await self.error_handlers.notify(self, update, e)
            if err:
                return err
            raise

    async def state_updater(self, update):
        state = await self.storage.get_state(
            chat=update.dialog.id,
            user=update.sender.id if hasattr(update, "sender") else update.dialog.id
        )
        context.update_state(
            user=update.sender.id if hasattr(update, "sender") else update.dialog.id,
            state=state
        )
