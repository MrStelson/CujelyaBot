from aiogram import executor

from loader import dp
import handlers
from utils.set_bot_commands import set_default_commands
from data_base import sqlite_db


async def on_startup(dispatcher):
    print('CujelyaBot online')
    sqlite_db.sql_start()
    await set_default_commands(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
