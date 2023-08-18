from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data_base.sqlite_db import sql_add_user
from loader import dp
from keyboards.client import mainKeyboard
from config import ADMIN_ID_FIRST, ADMIN_ID_SECOND

ADMIN_ID_LIST = [ADMIN_ID_FIRST, ADMIN_ID_SECOND]


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    username = '@' + message.from_user.username
    full_name = message.from_user.full_name
    chat_user_id = message.chat.id
    data_users = (user_id, username, full_name, None, None, 'available', chat_user_id)
    await sql_add_user(data_users)
    await message.delete()
    await message.answer(f"Привет, {full_name}!", reply_markup=mainKeyboard)
    if message.from_user.id in ADMIN_ID_LIST:
        await message.answer(f'Для перехода в админ режим нажми /start_admin')
