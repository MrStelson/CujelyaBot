from aiogram import types, F, Router
from aiogram.filters import Command

from config import CHAT_ID
from loader import bot
from keyboards.client import main_keyboard, cancel_keyboard, resume_keyboard

from states.States import FSMResume


user_resume_router = Router()


@user_resume_router.message(F.text == "Отправить резюме на разбор")
@user_resume_router.message(Command("resume"))
async def take_resume(message: types.Message, state: FSMResume):
    await state.set_state(FSMResume.resume)
    await message.reply(
        "Отправь резюме в формате .pdf\nДля отмены нажми кнопку или введи \n/cancel_resume",
        reply_markup=cancel_keyboard,
    )


# exit FSMQuestion
@user_resume_router.message(FSMResume.resume, F.text == "Отмена")
@user_resume_router.message(FSMResume.resume, Command("cancel_resume"))
async def cancel_handler_resume(message: types.Message, state: FSMResume):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.reply("Твое резюме не отправлено", reply_markup=main_keyboard)


@user_resume_router.message(FSMResume.resume, F.content_type.in_({"document"}))
async def take_resume_document(message: types.Message, state: FSMResume):
    await state.update_data(
        resume_id=message.document.file_id,
        username=message.from_user.username,
        fullname=message.from_user.full_name,
    )
    await message.answer(text="Отправить?", reply_markup=resume_keyboard)


@user_resume_router.callback_query(FSMResume.resume, F.data == "resume_false")
async def cancel_handler_resume_callback(
    callback: types.CallbackQuery, state: FSMResume
):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Твое резюме не отправлено", reply_markup=main_keyboard
    )
    await callback.answer()


@user_resume_router.callback_query(FSMResume.resume, F.data == "resume_true")
async def send_resume(callback: types.CallbackQuery, state: FSMResume):
    data = await state.get_data()
    file_id = data["resume_id"]
    username = data["username"]
    full_name = data["fullname"]
    await bot.send_document(
        CHAT_ID, document=file_id, caption=f"Резюме from {full_name} @{username}"
    )
    await callback.answer("Отправлено")
    await callback.message.delete()
    await callback.message.answer(
        text="Твое резюме отправлено\nОтвечу в течение 2-3х дней☀️",
        reply_markup=main_keyboard,
    )
    await state.clear()
