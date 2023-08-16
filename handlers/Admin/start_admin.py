from aiogram import types
from dotenv import load_dotenv, find_dotenv

from loader import dp
from keyboards.admin import adminMainKeyboard
from keyboards.client import mainKeyboard
from config import ADMIN_ID_FIRST, ADMIN_ID_SECOND

load_dotenv(find_dotenv())

ADMIN_ID_LIST = [ADMIN_ID_FIRST, ADMIN_ID_SECOND]


@dp.message_handler(commands=['start_admin'])
async def bot_admin_start(message: types.Message):
    await message.delete()
    if message.from_user.id in ADMIN_ID_LIST:
        await message.answer(f"Привет, админ {message.from_user.full_name}!", reply_markup=adminMainKeyboard)
    else:
        await message.answer(f'Вы не являетесь администратором', reply_markup=mainKeyboard)
