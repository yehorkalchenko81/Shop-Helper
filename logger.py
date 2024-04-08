import logging
import types
from collections.abc import Callable, Iterator
from functools import wraps

from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.event.telegram import TelegramEventObserver
from datetime import datetime

logger = logging.getLogger(__name__)


def _get_function_info(function: Callable, arg) -> str | None:
    if isinstance(function, types.FunctionType):
        name = function.__name__
        user = arg.from_user.full_name
        try:
            user_input = 'Text - ' + arg.text.replace('\n', ' \\n ') if isinstance(arg, Message) else 'CallBack - ' + arg.data
        except:
            user_input = 'None type'
        return f'Func: {name}, User_name: {user}, User_input: {user_input}, Time: {datetime.now()}'
    else:
        return None


def log_async_function(function: Callable):
    @wraps(function)
    async def wrapper(*args, **kwargs):
        function_info = _get_function_info(function, args[0])
        if function_info:
            with open('logs.txt', 'a', encoding='utf-8') as f:
                f.write(function_info + '\n')
        return await function(*args, **kwargs)

    return wrapper


def _enum_observers(router: Router) -> Iterator[TelegramEventObserver]:
    for _, value in vars(router).items():
        if isinstance(value, TelegramEventObserver):
            yield value


def decorate_callbacks(router: Router, decorator=log_async_function):
    for observer in _enum_observers(router):
        for handler in observer.handlers:
            handler.callback = decorator(handler.callback)

    for sub_router in router.sub_routers:
        decorate_callbacks(sub_router, decorator)
