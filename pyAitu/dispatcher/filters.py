import inspect
import re
from ..utils import context
from ..models import ContentType, Message

USER_STATE = 'USER_STATE'


async def check_filter(filter_, args):
    if not callable(filter_):
        raise TypeError('Filter must be callable and/or awaitable!')

    if inspect.isawaitable(filter_) or inspect.iscoroutinefunction(filter_):
        return await filter_(*args)
    else:
        return filter_(*args)


async def check_filters(filters, args):
    if filters is not None:
        for filter_ in filters:
            f = await check_filter(filter_, args)
            if not f:
                return False
    return True


def generate_default_filters(dispatcher, *args, **kwargs):
    filter_set = []

    for name, filter_ in kwargs.items():
        if filter_ is None and name != DefaultFilters.STATE:
            continue
        if name == DefaultFilters.COMMANDS:
            if isinstance(filter_, str):
                filter_set.append(CommandsFilter([filter_]))
            else:
                filter_set.append(CommandsFilter(filter_))
        elif name == DefaultFilters.CONTENT_TYPES:
            filter_set.append(ContentTypeFilter(filter_))
        elif name == DefaultFilters.REGEXP:
            filter_set.append(RegexpFilter(filter_))
        elif name == DefaultFilters.STATE:
            if isinstance(filter_, (list, set, tuple)):
                filter_set.append(StatesListFilter(dispatcher, filter_))
            else:
                filter_set.append(StateFilter(dispatcher, filter_))
        elif isinstance(filter_, Filter):
            filter_set.append(filter_)

    filter_set += list(args)

    return filter_set


class Filter:
    def __call__(self, *args, **kwargs):
        return self.check(*args, **kwargs)

    def check(self, *args, **kwargs):
        raise NotImplementedError


class AsyncFilter(Filter):
    def __aiter__(self):
        return None

    def __await__(self):
        return self.check

    async def check(self, *args, **kwargs):
        pass


class CommandsFilter(AsyncFilter):
    def __init__(self, commands):
        self.commands = commands

    async def check(self, message):
        if not message.is_command():
            return False

        command = message.text.split()[0][1:]
        command, _, mention = command.partition('@')

        if mention and mention != (await message.bot.me).username:
            return False

        if command not in self.commands:
            return False

        return True


class ContentTypeFilter(Filter):
    def __init__(self, content_types):
        self.content_types = content_types

    def check(self, message):
        return ContentType.ANY[0] in self.content_types or message.content_type in self.content_types


class RegexpFilter(Filter):
    def __init__(self, regexp):
        self.regexp = re.compile(regexp, flags=re.IGNORECASE | re.MULTILINE)

    def check(self, _object):
        if isinstance(_object, Message) and _object.text:
            return bool(self.regexp.search(_object.text))


class StateFilter(AsyncFilter):
    def __init__(self, dispatcher, state):
        self.dispatcher = dispatcher
        self.state = state

    def get_target(self, object_):
        return getattr(getattr(object_, 'chat', None), 'id', None), \
               getattr(getattr(object_, 'from_user', None), 'id', None)

    async def check(self, object_):
        if self.state == '*':
            return True

        if context.check_value(USER_STATE):
            context_state = context.get_value(USER_STATE)
            return self.state == context_state
        else:
            chat, user = self.get_target(object_)

            if chat or user:
                return await self.dispatcher.storage.get_state(chat=chat, user=user) == self.state
        return False


class StatesListFilter(StateFilter):
    async def check(self, object_):
        chat, user = self.get_target(object_)

        if chat or user:
            return await self.dispatcher.storage.get_state(chat=chat, user=user) in self.state
        return False


class DefaultFilters:
    COMMANDS = "commands"
    REGEXP = "regexp"
    CONTENT_TYPES = "content_types"
    FUNC = "func"
    STATE = "state"
