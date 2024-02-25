from aiogram import F, Router, types


from data_base.repository.feedback.feedback_repository_impl import \
    FeedbackRepositoryImplementation
from keyboards.admin import keyboard_delete_update


admin_show_feedback_router = Router()


@admin_show_feedback_router.message(F.text == "Показать все записи")
async def show_all_feedbacks(message: types.message):
    feedbacks = await FeedbackRepositoryImplementation.get_all_feedbacks()
    for feedback in feedbacks:
        keyboard = await keyboard_delete_update(feedback.id)
        await message.answer(
            text=f"Дата: {feedback.dateTimeFeedback.date()}\n"
            f"Время: {feedback.dateTimeFeedback.time()}\n"
            f"Статус: {feedback.status}\n"
            f"ID Пользователя: {feedback.user_id}\nПользователь: {feedback.username}",
            reply_markup=keyboard,
        )
    await message.answer("Все записи выведены")


@admin_show_feedback_router.message(F.text == "Показать активные записи")
async def show_all_active_feedbacks(message: types.message):
    feedbacks = await FeedbackRepositoryImplementation.get_all_booked_success_feedbacks()
    for feedback in feedbacks:
        keyboard = await keyboard_delete_update(feedback.id)
        await message.answer(
            text=f"Дата: {feedback.dateTimeFeedback.date()}\n"
            f"Время: {feedback.dateTimeFeedback.time()}\n"
            f"Статус: {feedback.status}\n"
            f"ID Пользователя: {feedback.user_id}\nПользователь: {feedback.username}",
            reply_markup=keyboard,
        )
    await message.answer("Все записи выведены")
