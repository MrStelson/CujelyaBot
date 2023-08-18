from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

mainKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
mainKeyboard. \
    row('Задать вопрос', 'Отправить резюме на разбор'). \
    add('Записаться на консультацию'). \
    row('Контакты', 'Помощь')

cancelKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
cancelKeyboard.add('Отмена')


async def feedback_keyboard_date(dates: dict, user_id):
    date_keyboard = InlineKeyboardMarkup(row_width=3)
    buttons_list = []
    for i in dates.keys():
        buttons_list.append(InlineKeyboardButton(text=f'{i}',
                                                 callback_data=f'date_{i}_{user_id}'))
    date_keyboard.add(*buttons_list)
    return date_keyboard


async def feedback_keyboard_time(times, user_id, date):
    time_keyboard = InlineKeyboardMarkup(row_width=2)
    buttons_list = []
    for i in times:
        buttons_list.append(InlineKeyboardButton(text=f'{i}',
                                                 callback_data=f'time_{i}_{date}_{user_id}'))
    time_keyboard.add(*buttons_list)
    time_keyboard.add(InlineKeyboardButton(text=f'←',
                                           callback_data=f'go_prev_date_{user_id}'))
    return time_keyboard


async def feedback_keyboard_success(date, time, user_id):
    btn_true = InlineKeyboardButton(text='Подтвердить',
                                    callback_data=f'feedback_success_{date}_{time}_{user_id}')
    btn_false = InlineKeyboardButton(text='Отменить', callback_data=f'feedback_canceled')
    keyboard_feedback_choice = InlineKeyboardMarkup().add(btn_true, btn_false)
    return keyboard_feedback_choice
