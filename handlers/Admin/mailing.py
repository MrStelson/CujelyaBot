from aiogram.dispatcher.filters import Text
from aiogram import types

from config import ADMIN_ID_FIRST, ADMIN_ID_SECOND
from loader import dp, bot
from data_base.sqlite_db import sql_admin_get_all_users_id
from states.States import FSMAdminMailing
from keyboards.admin import adminMainKeyboard, adminMailTrueFalseKeyboard
from keyboards.client import cancelKeyboard

ADMIN_ID_LIST = [ADMIN_ID_FIRST, ADMIN_ID_SECOND]


@dp.message_handler(Text(startswith='Сделать рассылку'), state=None)
async def mailing_for_all_users(message: types.message):
    if message.from_user.id in ADMIN_ID_LIST:
        await FSMAdminMailing.mail.set()
        await message.answer(text='Напиши текст рассылки\nДля отмены нажми кнопку', reply_markup=cancelKeyboard)
    else:
        await message.answer('Отказано в доступе')


@dp.message_handler(text='Отмена', state=FSMAdminMailing.mail)
async def cancel_handler_feedback_date(message: types.message, state: FSMAdminMailing):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Рассылка отменена", reply_markup=adminMainKeyboard)


@dp.message_handler(state=FSMAdminMailing.mail)
async def message_mail(message: types.message, state: FSMAdminMailing):
    text = message.text
    async with state.proxy() as data:
        data['mail'] = text
    await FSMAdminMailing.success.set()
    await message.answer(f'Отправить?', reply_markup=adminMailTrueFalseKeyboard)


@dp.callback_query_handler(text='mail_admin_false', state=FSMAdminMailing.success)
async def cancel_handler_feedback_date(callback: types.callback_query, state: FSMAdminMailing):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.message.delete()
    await callback.message.answer("Рассылка отменена", reply_markup=adminMainKeyboard)


@dp.callback_query_handler(text='mail_admin_true', state=FSMAdminMailing.success)
async def send_mail(callback: types.callback_query, state: FSMAdminMailing):
    user_id_list = await sql_admin_get_all_users_id()
    async with state.proxy() as data:
        text = data['mail']
    for user_id in user_id_list:
        await bot.send_message(chat_id=user_id[0], text=text)
    await state.finish()
    await callback.message.delete()
    await callback.message.answer(f'Рассылка отправлена {len(user_id_list)} пользователям',
                                     reply_markup=adminMainKeyboard)
