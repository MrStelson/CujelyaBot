"""Модуль промежуточного слоя для обработки исключений"""

from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from config import CHAT_ID
from loader import bot


class ExceptMiddleware(BaseMiddleware):
    """Класс промежуточного слоя для обработки исключений"""

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as error:
            await bot.send_message(
                CHAT_ID,
                text=f"Error ❗️\n"
                     f"User: @{event.from_user.username} {event.from_user.full_name}\n"
                     f"Command: {event.text}\n"
                     f"Error: {error}",
            )
