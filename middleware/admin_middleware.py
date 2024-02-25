"""Модуль промежуточного слоя для авторизации администратора"""

from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from config import ADMIN_ID_LIST


class AdminMiddleware(BaseMiddleware):
    """Класс промежуточного слоя для авторизации администратора"""

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.from_user.id in ADMIN_ID_LIST:
            return await handler(event, data)

        return event.answer("Отказано")
