from aiogram import types
from aiogram.dispatcher.filters import Text
from data_base.sqlite_db import sql_admin_delete_feedback, sql_admin_delete_passed_feedback
from keyboards.admin import keyboard_delete_success, keyboard_delete_update
from loader import dp
from config import ADMIN_ID_FIRST, ADMIN_ID_SECOND

ADMIN_ID_LIST = [ADMIN_ID_FIRST, ADMIN_ID_SECOND]

@dp.callback_query_handler(Text(startswith='delete_choice_'))
async def delete_feedback(callback: types.CallbackQuery):
    id_feedback = callback.data.split("_")[-1]
    keyboard_success = await keyboard_delete_success(id_feedback)
    await callback.message.edit_reply_markup(reply_markup=keyboard_success)


@dp.callback_query_handler(Text(startswith='delete_true_'))
async def delete_feedback_success(callback: types.CallbackQuery):
    id_feedback = callback.data.split("_")[-1]
    await sql_admin_delete_feedback(id_feedback=id_feedback)
    await callback.message.edit_text('Запись удалена')


@dp.callback_query_handler(Text(startswith='delete_false_'))
async def delete_feedback_cancel(callback: types.CallbackQuery):
    id_feedback = callback.data.split("_")[-1]
    keyboard = await keyboard_delete_update(id_feedback)
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@dp.message_handler(Text(startswith='Удалить прошедшие записи'))
async def delete_all_last_feedback(message: types.message):
    if message.from_user.id in ADMIN_ID_LIST:
        await sql_admin_delete_passed_feedback()
        await message.answer(text="Прошедшие даты удалены")
    else:
        await message.answer(text='Отказано в доступе')