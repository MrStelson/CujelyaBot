from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(text='Помощь')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/help - Получить справку",
            "/question - Задать вопрос Кужеле",
            "/resume - Отправить резюме для разбора",
            "/feedback - Записаться на консультацию"
            )
    await message.answer("\n".join(text))
