from typing import List

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from data_base.models.feedback import Feedback

main_keyboard_buttons = [
    [
        KeyboardButton(text="Задать вопрос"),
        KeyboardButton(text="Отправить резюме на разбор"),
    ],
    [KeyboardButton(text="Записаться на консультацию")],
    [KeyboardButton(text="Контакты"), KeyboardButton(text="Помощь")],
]
main_keyboard = ReplyKeyboardMarkup(
    keyboard=main_keyboard_buttons, resize_keyboard=True
)

cancel_keyboard_buttons = [[KeyboardButton(text="Отмена")]]
cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=cancel_keyboard_buttons, resize_keyboard=True
)


success_question = InlineKeyboardButton(text="Отправить", callback_data="question_true")
cancel_question = InlineKeyboardButton(text="Отменить", callback_data="question_false")
question_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[success_question, cancel_question]]
)

portfolio_button = InlineKeyboardButton(
    text="Мое портфолио", web_app=WebAppInfo(url="https://www.artstation.com/cujel")
)
portfolio_keyboard = InlineKeyboardMarkup(inline_keyboard=[[portfolio_button]])


success_resume = InlineKeyboardButton(text="Отправить", callback_data="resume_true")
cancel_resume = InlineKeyboardButton(text="Отменить", callback_data="resume_false")
resume_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[success_resume, cancel_resume]]
)


async def feedback_keyboard_date(feedbacks: List[Feedback], user_id: int):
    date_keyboard = InlineKeyboardBuilder()
    buttons_list = []

    for feedback in feedbacks:
        date = feedback.dateTimeFeedback.date()
        buttons_list.append(
            InlineKeyboardButton(text=f"{date}", callback_data=f"date_{date}_{user_id}")
        )

    # for i in dates.keys():
    #     buttons_list.append(
    #         InlineKeyboardButton(text=f"{i}", callback_data=f"date_{i}_{user_id}")
    #     )
    date_keyboard.row(*buttons_list, width=3)
    return date_keyboard.as_markup()


async def feedback_keyboard_time(feedbacks: List[Feedback], user_id: int):
    time_keyboard = InlineKeyboardBuilder()
    buttons_list = []
    for feedback in feedbacks:
        feedback_time = feedback.dateTimeFeedback.time()
        feedback_date = feedback.dateTimeFeedback.date()
        buttons_list.append(
            InlineKeyboardButton(
                text=f"{feedback_time}", callback_data=f"time_{feedback_time}_{feedback_date}_{user_id}"
            )
        )
    time_keyboard.row(*buttons_list, width=3)

    buttons = time_keyboard.export()
    buttons.append([InlineKeyboardButton(text=f"←", callback_data=f"go_prev_date_{user_id}")])
    InlineKeyboardMarkup(inline_keyboard=buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def feedback_keyboard_success(date: str, time: str, user_id: str):
    btn_true = InlineKeyboardButton(
        text="Подтвердить", callback_data=f"feedback_success_{date}_{time}_{user_id}"
    )
    btn_false = InlineKeyboardButton(
        text="Отменить", callback_data=f"feedback_canceled"
    )
    keyboard_feedback_choice = InlineKeyboardMarkup(
        inline_keyboard=[[btn_true, btn_false]]
    )
    return keyboard_feedback_choice
