from aiogram import types
from loader import dp


@dp.message_handler(text='Контакты')
async def get_contacts(message: types.message):
    await message.reply('Мои контакты')
