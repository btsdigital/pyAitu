import asyncio
from typing import Dict, Coroutine

CONFIGURED = '@CONFIGURED_TASK_FACTORY'


def task_factory(loop: asyncio.BaseEventLoop, coroutine: Coroutine):
    if loop.is_closed():
        raise RuntimeError('Event loop is closed')

    task = asyncio.Task(coroutine, loop=loop)

    try:
        task.context = asyncio.Task.current_task().context.copy()
    except AttributeError:
        task.context = {CONFIGURED: True}

    return task


def set_value(key, value):
    get_current_state()[key] = value


def get_current_state() -> Dict:
    task = asyncio.Task.current_task()
    if task is None:
        raise RuntimeError('Can be used only in Task context.')
    context_ = getattr(task, 'context', None)
    if context_ is None:
        context_ = task.context = {}
    return context_


def update_state(data=None, **kwargs):
    if data is None:
        data = {}
    state = get_current_state()
    state.update(data, **kwargs)


def check_value(key):
    return key in get_current_state()


def get_value(key, default=None):
    return get_current_state().get(key, default)
