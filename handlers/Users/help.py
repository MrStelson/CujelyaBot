from aiogram import types, F
from aiogram.filters import Command
from aiogram import Router
from data_base.repository.user.user_repository_impl import UserRepositoryImplementation

from data_base.shemas.user import UserDto

user_help_router = Router()


@user_help_router.message(F.text == "Помощь")
@user_help_router.message(Command("help"))
async def bot_help(message: types.Message):

    text = (
        "Список команд: ",
        "/help - Получить справку",
        "/question - Задать вопрос Кужеле",
        "/resume - Отправить резюме для разбора",
        "/feedback - Записаться на консультацию",
    )
    await message.answer("\n".join(text))
