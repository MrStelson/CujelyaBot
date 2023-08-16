from aiogram import types
from aiogram.dispatcher.filters import Text
from data_base.sqlite_db import sql_admin_update_status, get_date_time
from keyboards.admin import keyboard_update_success, keyboard_delete_update
from loader import dp


@dp.callback_query_handler(Text(startswith='update_choice_'))
async def update_choice(callback: types.CallbackQuery):
    id_feedback = callback.data.split("_")[-1]
    keyboard_status = await keyboard_update_success(id_feedback)
    await callback.message.edit_reply_markup(reply_markup=keyboard_status)


@dp.callback_query_handler(Text(startswith='update_status_'))
async def update_status(callback: types.CallbackQuery):
    id_feedback = callback.data.split("_")[-1]
    status = callback.data.split("_")[-2]
    keyboard = await keyboard_delete_update(id_feedback)
    feedback = await sql_admin_update_status(id_feedback, status)
    date_time = await get_date_time(feedback[1])
    await callback.message.edit_text(text=f'Дата: {date_time["date"]}\n'
                                          f'Время: {date_time["time"]}\n'
                                          f'Статус: {feedback[2]}\n'
                                          f'Пользователь: {feedback[3]}\nПользователь: {feedback[4]}',
                                     reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='update_false_'))
async def update_status_cancel(callback: types.CallbackQuery):
    id_feedback = callback.data.split("_")[-1]
    keyboard = await keyboard_delete_update(id_feedback)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
