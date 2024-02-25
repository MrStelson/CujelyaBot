from aiogram import F, types, Router
from keyboards.client import portfolio_keyboard

user_contracts_router = Router()


@user_contracts_router.message(F.text == "Контакты")
async def get_contacts(message: types.message):
    await message.answer(
        "Мои контакты:\nЛичный тг-канал: @cujel\nПочта: cujelya@gmail.com",
        reply_markup=portfolio_keyboard,
    )
