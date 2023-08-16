from aiogram import types
from data_base.sqlite_db import sql_admin_show_all_feedbacks, sql_admin_show_booked_feedbacks, get_date_time
from keyboards.admin import keyboard_delete_update
from loader import dp
from config import ADMIN_ID_FIRST, ADMIN_ID_SECOND

ADMIN_ID_LIST = [ADMIN_ID_FIRST, ADMIN_ID_SECOND]

@dp.message_handler(text='Показать все записи')
async def show_all_feedbacks(message: types.message):
    if message.from_user.id in ADMIN_ID_LIST:
        data = await sql_admin_show_all_feedbacks()
        for entry in data.fetchall():
            keyboard = await keyboard_delete_update(entry[0])
            date_time = await get_date_time(entry[1])
            await message.answer(text=f'Дата: {date_time["date"]}\n'
                                      f'Время: {date_time["time"]}\n'
                                      f'Статус: {entry[2]}\n'
                                      f'ID Пользователя: {entry[3]}\nПользователь: {entry[4]}',
                                 reply_markup=keyboard)
        await message.answer('Все записи выведены')
    else:
        await message.answer('Отказано')


@dp.message_handler(text='Показать активные записи')
async def show_all_active_feedbacks(message: types.message):
    if message.from_user.id in ADMIN_ID_LIST:
        data, len_data = await sql_admin_show_booked_feedbacks()
        if len_data == (0,):
            await message.answer('Активных записей нет')
        else:
            for entry in data.fetchall():
                keyboard = await keyboard_delete_update(entry[0])
                date_time = await get_date_time(entry[1])
                await message.answer(text=f'Дата: {date_time["date"]}\n'
                                          f'Время: {date_time["time"]}\n'
                                          f'Статус: {entry[2]}\n'
                                          f'ID Пользователя: {entry[3]}\nПользователь: {entry[4]}',
                                     reply_markup=keyboard)
            await message.answer('Все записи выведены')
    else:
        await message.answer('Отказано')
