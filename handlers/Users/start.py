from aiogram import Router, types
from aiogram.filters import CommandStart

from data_base.repository.user.user_repository_impl import UserRepositoryImplementation
from data_base.shemas.user import UserDto
from keyboards.client import main_keyboard
from config import ADMIN_ID_LIST

user_start_router = Router()


@user_start_router.message(CommandStart())
async def bot_start(message: types.Message):

    user = await UserRepositoryImplementation.get_or_create_user(
        user=UserDto(
            id=message.from_user.id,
            username="@" + message.from_user.username,
            fullname=message.from_user.full_name,
            status="available",
            id_feedback=None,
            dateTimeFeedback=None,
        )
    )

    await message.delete()
    await message.answer(
        f"Привет, {message.from_user.full_name}!", reply_markup=main_keyboard
    )

    if message.from_user.id in ADMIN_ID_LIST:
        await message.answer(f"Для перехода в админ режим нажми /start_admin")
