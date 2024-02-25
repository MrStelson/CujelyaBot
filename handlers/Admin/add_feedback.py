import re
from datetime import datetime

from aiogram import F, Router, types

from data_base.repository.feedback.feedback_repository_impl import (
    FeedbackRepositoryImplementation,
)
from data_base.shemas.feedback import FeedbackAddDto
from keyboards.admin import admin_main_keyboard
from keyboards.client import cancel_keyboard
from states.States import FSMAdminAddFeedback

admin_add_feedback_router = Router()


def is_valid_date(input_date):
    try:
        reg_data = r"[0-3][0-9][.][0-1][0-9]"
        day = input_date.split(".")[0]
        month = input_date.split(".")[1]
        day_month = f"2023-{month}-{day}"
        datetime.strptime(day_month, "%Y-%m-%d")
        return bool(re.search(reg_data, input_date))
    except Exception:
        return False


def is_valid_time(input_date):
    try:
        reg_time = r"[0-2][0-9][:][0-5][0-9]"
        hours = input_date.split(":")[0]
        minutes = input_date.split(":")[1]
        day_month = f"{hours}-{minutes}"
        datetime.strptime(day_month, "%H-%M")
        return bool(re.search(reg_time, input_date))
    except Exception:
        return False


@admin_add_feedback_router.message(F.text == "Добавить запись")
async def add_feedback_start(message: types.message, state: FSMAdminAddFeedback):
    await state.set_state(FSMAdminAddFeedback.date)
    await message.answer(
        "Напиши дату в формате ДД.ММ\nДля отмены нажми кнопку",
        reply_markup=cancel_keyboard,
    )


# exit
@admin_add_feedback_router.message(FSMAdminAddFeedback.date, F.text == "Отмена")
async def cancel_handler_feedback_date(
    message: types.message, state: FSMAdminAddFeedback
):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.reply("Запись отменена", reply_markup=admin_main_keyboard)


@admin_add_feedback_router.message(FSMAdminAddFeedback.date)
async def add_feedback_date(message: types.message, state: FSMAdminAddFeedback):
    await state.update_data(date=message.text, user_message_date=message)
    if is_valid_date(message.text):
        await message.answer(
            "Напиши время в формате ЧЧ:ММ\nДля отмены нажми кнопку",
            reply_markup=cancel_keyboard,
        )
        await state.set_state(FSMAdminAddFeedback.time)
    else:
        await message.answer("Неправильный формат даты.")
        await add_feedback_start(message=message, state=state)


# exit
@admin_add_feedback_router.message(FSMAdminAddFeedback.time, F.text == "Отмена")
async def cancel_handler_feedback_time(
    message: types.message, state: FSMAdminAddFeedback
):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Запись отменена", reply_markup=admin_main_keyboard)


@admin_add_feedback_router.message(FSMAdminAddFeedback.time)
async def add_feedback_time(message: types.message, state: FSMAdminAddFeedback):
    data = await state.get_data()
    data["time"] = message.text

    if is_valid_time(data["time"]):
        day, month = data.get("date").split(".")
        hour, minute = data.get("time").split(":")

        feedback_datetime = datetime(
            year=datetime.now().year,
            month=int(month),
            day=int(day),
            hour=int(hour),
            minute=int(minute),
        )

        await FeedbackRepositoryImplementation.create_feedback(
            feedback_add_dto=FeedbackAddDto(dateTimeFeedback=feedback_datetime)
        )

        await message.answer("Дата добавлена!", reply_markup=admin_main_keyboard)
        await state.clear()
    else:
        await message.answer("Неправильный формат времени.")
        await add_feedback_date(message=data["user_message_date"], state=state)
