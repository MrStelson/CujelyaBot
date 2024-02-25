"""Модуль инициализации приложения"""

import asyncio

from aiogram import Dispatcher
from handlers import user_routers, admin_routers
from loader import bot, on_startup
from middleware import AdminMiddleware, ExceptMiddleware

ALLOWED_UPDATES = ["message, edited_message"]


async def setup_bot_settings():
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.include_routers(*user_routers)
    dp.include_routers(*admin_routers)

    for admin_router in admin_routers:
        admin_router.message.middleware(AdminMiddleware())
        admin_router.message.middleware(ExceptMiddleware())

    for user_router in user_routers:
        user_router.message.middleware(ExceptMiddleware())

    return dp


async def main():
    dp = await setup_bot_settings()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    asyncio.run(main())
