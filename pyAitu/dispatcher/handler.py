from .filters import check_filters
from ..utils import context


class SkipHandler(BaseException):
    pass


class CancelHandler(BaseException):
    pass


class Handler:
    def __init__(self, dispatcher, once=True, middleware_key=None):
        self.dispatcher = dispatcher
        self.middleware_key = middleware_key
        self.once = once
        self.handlers = []

    def register(self, handler, filters=None, index=None):
        if filters and not isinstance(filters, (list, tuple, set)):
            filters = [filters]
        record = (filters, handler)
        if index is None:
            self.handlers.append(record)
        else:
            self.handlers.insert(index, record)

    def unregister(self, handler):
        for handler_with_filters in self.handlers:
            _, registered = handler_with_filters
            if handler is registered:
                self.handlers.remove(handler_with_filters)
                return True
        raise ValueError('This handler is not registered')

    async def notify(self, *args):
        results = []

        if self.middleware_key:
            try:
                await self.dispatcher.middleware.trigger(f"pre_process_{self.middleware_key}", args)
            except CancelHandler:
                return results

        for filters, handler in self.handlers:
            if await check_filters(filters, args):
                try:
                    if self.middleware_key:
                        context.set_value('handler', handler)
                        await self.dispatcher.middleware.trigger(f"process_{self.middleware_key}", args)
                    response = await handler(*args)
                    if response is not None:
                        results.append(response)
                    if self.once:
                        break
                except SkipHandler:
                    continue
                except CancelHandler:
                    break

        if self.middleware_key:
            await self.dispatcher.middleware.trigger(f"post_process_{self.middleware_key}", args + (results,))

        return results
