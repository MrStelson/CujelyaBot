from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

admin_main_keyboard_buttons = [
    [
        KeyboardButton(text="Добавить запись"),
        KeyboardButton(text="Удалить прошедшие записи"),
    ],
    [
        KeyboardButton(text="Показать все записи"),
        KeyboardButton(text="Показать активные записи"),
    ],
    [
        KeyboardButton(text="Сделать рассылку"),
        KeyboardButton(text="Вывести всех пользователей"),
    ],
    [
        KeyboardButton(text="Сжать изображение"),
    ],
]
admin_main_keyboard = ReplyKeyboardMarkup(
    keyboard=admin_main_keyboard_buttons, resize_keyboard=True
)

mail_true = InlineKeyboardButton(text="Подтвердить", callback_data="mail_admin_true")
mail_false = InlineKeyboardButton(text="Отменить", callback_data="mail_admin_false")
admin_mail_true_false_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[mail_true, mail_false]]
)


async def keyboard_delete_update(id_feedback: int):
    keyboard_delete_builder = InlineKeyboardBuilder()
    keyboard_delete_builder.add(
        InlineKeyboardButton(
            text="↑ Удалить ↑", callback_data=f"delete_choice_{id_feedback}"
        ),
        InlineKeyboardButton(
            text="↑ Изменить статус ↑", callback_data=f"update_choice_{id_feedback}"
        ),
    )
    return keyboard_delete_builder.as_markup()


async def keyboard_delete_success(id_feedback):
    keyboard_delete_choice_builder = InlineKeyboardBuilder()
    btn_true = InlineKeyboardButton(
        text="Подтвердить", callback_data=f"delete_true_{id_feedback}"
    )
    btn_false = InlineKeyboardButton(
        text="Отменить", callback_data=f"delete_false_{id_feedback}"
    )
    keyboard_delete_choice_builder.row(btn_true, btn_false)
    return keyboard_delete_choice_builder.as_markup()


async def keyboard_update_success(id_feedback):
    keyboard_update_choice_builder = InlineKeyboardBuilder()
    btn_available = InlineKeyboardButton(
        text="available", callback_data=f"update_status_available_{id_feedback}"
    )
    btn_booked = InlineKeyboardButton(
        text="booked", callback_data=f"update_status_booked_{id_feedback}"
    )
    btn_success = InlineKeyboardButton(
        text="success", callback_data=f"update_status_success_{id_feedback}"
    )
    btn_false = InlineKeyboardButton(
        text="Отменить", callback_data=f"update_false_{id_feedback}"
    )
    keyboard_update_choice_builder.row(
        btn_available, btn_booked, btn_success, btn_false, width=3
    )
    return keyboard_update_choice_builder.as_markup()
