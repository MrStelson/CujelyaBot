from aiogram import types
from aiogram.dispatcher.filters import Text

from data_base.sqlite_db import sql_show_feedbacks, sql_check_user_status, sql_get_feedback, sql_book_feedback, \
    sql_admin_get_user, get_date_time
from loader import dp, bot
from keyboards.client import feedback_keyboard_date, feedback_keyboard_time, feedback_keyboard_success
from config import CHAT_ID


@dp.message_handler(commands=['feedback'], state=None)
@dp.message_handler(text='Записаться на консультацию', state=None)
async def show_all_feedbacks_dates(message: types.message):
    user_id = message.from_user.id
    user = await sql_check_user_status(user_id)
    if user[-2] == 'available':
        data = await sql_show_feedbacks()
        keyboard = await feedback_keyboard_date(data, user_id)
        if data:
            await message.answer(f'Выбери дату', reply_markup=keyboard)
        else:
            await message.answer(f'Свободных слотов нет')
    else:
        date_time = await get_date_time(user[4])
        await message.answer(f'Вы уже записаны на {date_time["date"]} в {date_time["time"]} Мск')


@dp.callback_query_handler(Text(startswith='date_'))
async def show_all_feedbacks_times(callback: types.CallbackQuery):
    date = callback.data.split("_")[1]
    data = await sql_show_feedbacks()
    user_id = callback.data.split("_")[2]
    keyboard = await feedback_keyboard_time(times=sorted(data[date]), date=date, user_id=user_id)
    await callback.message.edit_text(f'Выбери время Мск', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='go_prev_date'))
async def go_prev_date(callback: types.CallbackQuery):
    user_id = callback.data.split("_")[-1]
    data = await sql_show_feedbacks()
    keyboard = await feedback_keyboard_date(data, user_id=user_id)
    await callback.message.edit_text(f'Выбери дату', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='time_'))
async def get_feedback_time(callback: types.CallbackQuery):
    date_time = callback.data.split('_')
    time = date_time[1]
    date = date_time[2]
    user_id = date_time[3]
    keyboard = await feedback_keyboard_success(date=date, time=time, user_id=user_id)
    await callback.message.edit_text(text=f'Дата: {date}. Время: {time} Мск', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='feedback_success_'))
async def feedback_success(callback: types.CallbackQuery):
    date = callback.data.split("_")[2]
    time = callback.data.split("_")[3]
    user_id = callback.data.split("_")[4]
    feedback = await sql_get_feedback(date, time)
    if feedback[2] == 'available':
        await sql_book_feedback(date, time, int(user_id))
        await callback.message.edit_text(text=f'Вы записаны на {date} в {time} Мск')
        user = await sql_admin_get_user(user_id)
        await bot.send_message(CHAT_ID, text=f'{user[1]} Записался на {date} в {time} Мск')
    else:
        await callback.message.delete()
        await callback.message.answer('Запись уже занята')


@dp.callback_query_handler(Text(startswith='feedback_canceled'))
async def feedback_success(callback: types.CallbackQuery):
    await callback.message.answer('Запись отменена')
    await callback.message.delete()
