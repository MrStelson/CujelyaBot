from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

adminMainKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
adminMainKeyboard. \
    row('Добавить запись', 'Удалить прошедшие записи'). \
    row('Показать все записи', 'Показать активные записи'). \
    add('Сделать рассылку')

adminMailTrueFalseKeyboard = InlineKeyboardMarkup(resize_keyboard=True)
mailTrue = InlineKeyboardButton(text='Подтвердить', callback_data='mail_admin_true')
mailFalse = InlineKeyboardButton(text='Отменить', callback_data='mail_admin_false')
adminMailTrueFalseKeyboard.row(mailTrue, mailFalse)


async def keyboard_delete_update(id_feedback):
    keyboard_delete_btn = InlineKeyboardMarkup()
    keyboard_delete_btn.add(InlineKeyboardButton(text='↑ Удалить ↑', callback_data=f'delete_choice_{id_feedback}'),
                            InlineKeyboardButton(text='↑ Изменить статус ↑',
                                                 callback_data=f'update_choice_{id_feedback}'))
    return keyboard_delete_btn


async def keyboard_delete_success(id_feedback):
    keyboard_delete_choice = InlineKeyboardMarkup()
    btn_true = InlineKeyboardButton(text='Подтвердить', callback_data=f'delete_true_{id_feedback}')
    btn_false = InlineKeyboardButton(text='Отменить', callback_data=f'delete_false_{id_feedback}')
    keyboard_delete_choice.row(btn_true, btn_false)
    return keyboard_delete_choice


async def keyboard_update_success(id_feedback):
    keyboard_update_choice = InlineKeyboardMarkup()
    btn_available = InlineKeyboardButton(text='available', callback_data=f'update_status_available_{id_feedback}')
    btn_booked = InlineKeyboardButton(text='booked', callback_data=f'update_status_booked_{id_feedback}')
    btn_success = InlineKeyboardButton(text='success', callback_data=f'update_status_success_{id_feedback}')
    btn_false = InlineKeyboardButton(text='Отменить', callback_data=f'update_false_{id_feedback}')
    keyboard_update_choice.row(btn_available, btn_booked, btn_success).add(btn_false)
    return keyboard_update_choice
