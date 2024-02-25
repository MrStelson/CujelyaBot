from datetime import datetime, timedelta

from aiogram import F, Router, types
from aiogram.filters import Command

from config import CHAT_ID, HOUR_OFFSET
from data_base.repository.feedback.feedback_repository_impl import (
    FeedbackRepositoryImplementation,
)
from data_base.repository.user.user_repository_impl import UserRepositoryImplementation
from data_base.shemas.user import UserDto
from keyboards.client import (
    feedback_keyboard_date,
    feedback_keyboard_success,
    feedback_keyboard_time,
)
from loader import bot

user_feedback_router = Router()


@user_feedback_router.message(Command("feedback"))
@user_feedback_router.message(F.text == "Записаться на консультацию")
async def show_all_feedbacks_dates(message: types.message):
    user_id = message.from_user.id

    user = await UserRepositoryImplementation.get_user_by_id(user_id=user_id)

    datetime_now = datetime.now() - timedelta(hours=HOUR_OFFSET)

    if (user_time_feedback := user.dateTimeFeedback) and user_time_feedback <= datetime_now:
        user = await UserRepositoryImplementation.update_user(
            user_dto=UserDto(
                id=user.id,
                username=user.username,
                fullname=user.fullname,
                status="available",
                id_feedback=None,
                dateTimeFeedback=None,
            )
        )

    if user.status == "available":
        if (
            feedbacks := await FeedbackRepositoryImplementation.get_all_active_feedback()
        ):
            keyboard = await feedback_keyboard_date(feedbacks, user_id)
            await message.answer(f"Выбери дату", reply_markup=keyboard)
        else:
            await message.answer(f"Свободных слотов нет")

    else:
        date_time = user.dateTimeFeedback
        await message.answer(
            f"Вы уже записаны на {date_time.date()} в {date_time.time()} Мск"
        )


@user_feedback_router.callback_query(F.data.startswith("date_"))
async def show_all_feedbacks_times(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[2])
    feedback_date = datetime.strptime(callback.data.split("_")[1], "%Y-%m-%d")

    feedbacks = await FeedbackRepositoryImplementation.get_feedbacks_by_date(
        feedback_date=feedback_date
    )

    keyboard = await feedback_keyboard_time(feedbacks=feedbacks, user_id=user_id)
    await callback.message.edit_text(f"Выбери время Мск", reply_markup=keyboard)
    await callback.answer()


@user_feedback_router.callback_query(F.data.startswith("go_prev_date"))
async def go_prev_date(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[-1])
    feedbacks = await FeedbackRepositoryImplementation.get_all_active_feedback()
    keyboard = await feedback_keyboard_date(feedbacks=feedbacks, user_id=user_id)
    await callback.message.edit_text(f"Выбери дату", reply_markup=keyboard)
    await callback.answer()


@user_feedback_router.callback_query(F.data.startswith("time_"))
async def get_feedback_time(callback: types.CallbackQuery):
    date_time = callback.data.split("_")
    time = date_time[1]
    date = date_time[2]
    user_id = date_time[3]
    keyboard = await feedback_keyboard_success(date=date, time=time, user_id=user_id)
    await callback.message.edit_text(
        text=f"Дата: {date}. Время: {time} Мск", reply_markup=keyboard
    )


@user_feedback_router.callback_query(F.data.startswith("feedback_success_"))
async def feedback_success(callback: types.CallbackQuery):
    date = callback.data.split("_")[2]
    time = callback.data.split("_")[3]
    user_id = int(callback.data.split("_")[4])

    feedback_datetime = datetime.strptime(f"{date}_{time}", "%Y-%m-%d_%H:%M:%S")
    feedback = await FeedbackRepositoryImplementation.get_feedback_by_datetime(
        feedback_datetime=feedback_datetime
    )

    if feedback.status == "available":
        await FeedbackRepositoryImplementation.update_feedback_status(
            feedback_id=feedback.id, status="booked"
        )

        user = await UserRepositoryImplementation.get_user_by_id(user_id=user_id)
        user = await UserRepositoryImplementation.update_user(
            user_dto=UserDto(
                id=user.id,
                username=user.username,
                fullname=user.fullname,
                status="booked",
                id_feedback=feedback.id,
                dateTimeFeedback=feedback.dateTimeFeedback,
            )
        )

        await callback.message.edit_text(text=f"Вы записаны на {date} в {time} Мск")
        await bot.send_message(
            CHAT_ID,
            text=f"{user.username} {user.fullname} Записался на {date} в {time} Мск",
        )
    else:
        await callback.message.delete()
        await callback.message.answer("Запись уже занята")


@user_feedback_router.callback_query(F.data.startswith("feedback_canceled"))
async def feedback_success(callback: types.CallbackQuery):
    await callback.message.answer("Запись отменена")
    await callback.message.delete()
