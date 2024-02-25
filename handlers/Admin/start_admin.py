from aiogram import types, Router
from aiogram.filters import Command

from keyboards.admin import admin_main_keyboard

admin_start_router = Router()


@admin_start_router.message(Command('start_admin'))
async def bot_admin_start(message: types.Message):
    await message.answer(f"Привет, админ {message.from_user.full_name}!", reply_markup=admin_main_keyboard)

