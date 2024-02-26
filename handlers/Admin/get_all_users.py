from aiogram import F, Router, types

from data_base.repository.user.user_repository_impl import UserRepositoryImplementation

admin_get_all_users_router = Router()


@admin_get_all_users_router.message(F.text == "Вывести всех пользователей")
async def get_all_users(message: types.message):
    users = await UserRepositoryImplementation.get_all_user()
    users_string = ""
    for index, user in enumerate(users, 1):
        users_string += f"{index}. {user.username} {user.fullname}\n"
    await message.answer(text=f"{users_string}")
