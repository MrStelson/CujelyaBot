from aiogram import types
from loader import dp
from states.States import FSMAddFeedback
from keyboards.admin import adminMainKeyboard
from keyboards.client import cancelKeyboard
from config import ADMIN_ID_FIRST, ADMIN_ID_SECOND
from data_base import sqlite_db
import re
from datetime import datetime

ADMIN_ID_LIST = [ADMIN_ID_FIRST, ADMIN_ID_SECOND]

def is_valid_date(input_date):
    try:
        reg_data = r'[0-3][0-9][.][0-1][0-9]'
        day = input_date.split('.')[0]
        month = input_date.split('.')[1]
        day_month = f'2023-{month}-{day}'
        datetime.strptime(day_month, '%Y-%m-%d')
        return bool(re.search(reg_data, input_date))
    except Exception:
        return False


def is_valid_time(input_date):
    try:
        reg_time = r'[0-2][0-9][:][0-5][0-9]'
        hours = input_date.split(':')[0]
        minutes = input_date.split(':')[1]
        day_month = f'{hours}-{minutes}'
        datetime.strptime(day_month, '%H-%M')
        return bool(re.search(reg_time, input_date))
    except Exception:
        return False


@dp.message_handler(text='Добавить запись', state=None)
async def add_feedback_start(message: types.message):
    if message.from_user.id in ADMIN_ID_LIST:
        await FSMAddFeedback.date.set()
        await message.answer('Напиши дату в формате ДД.ММ\nДля отмены нажми кнопку',
                             reply_markup=cancelKeyboard)
    else:
        await message.answer('Вам запрещено добавлять записи!')


# exit
@dp.message_handler(text='Отмена', state=FSMAddFeedback.date)
async def cancel_handler_feedback_date(message: types.message, state: FSMAddFeedback):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Запись отменена", reply_markup=adminMainKeyboard)


@dp.message_handler(state=FSMAddFeedback.date)
async def add_feedback_date(message: types.message, state: FSMAddFeedback):
    if message.from_user.id in ADMIN_ID_LIST:
        async with state.proxy() as data:
            data['date'] = message.text
            data['user_message_date'] = message
        if is_valid_date(data['date']):
            await message.answer('Напиши время в формате ЧЧ:ММ\nДля отмены нажми кнопку', reply_markup=cancelKeyboard)
            await FSMAddFeedback.time.set()
        else:
            await message.answer('Неправильный формат даты.')
            await add_feedback_start(message)
    else:
        await message.answer('Вам запрещено добавлять записи!')


# exit
@dp.message_handler(text='Отмена', state=FSMAddFeedback.time)
async def cancel_handler_feedback_time(message: types.message, state: FSMAddFeedback):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Запись отменена", reply_markup=adminMainKeyboard)


@dp.message_handler(state=FSMAddFeedback.time)
async def add_feedback_time(message: types.message, state: FSMAddFeedback):
    if message.from_user.id in ADMIN_ID_LIST:
        async with state.proxy() as data:
            data['time'] = message.text
            data['status'] = 'available'
            data['user_id'] = None
            data['username'] = None
        if is_valid_time(data["time"]):
            await message.answer('Дата добавлена!', reply_markup=adminMainKeyboard)
            await sqlite_db.sql_add_feedback(data)
            await state.finish()
        else:
            await message.answer('Неправильный формат времени.')
            await add_feedback_date(message=data['user_message_date'], state=state)
    else:
        await message.answer('Вам запрещено добавлять записи!')
