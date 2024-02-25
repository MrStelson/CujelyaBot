""""""

from aiogram import F, Router, types

from data_base.repository.feedback.feedback_repository_impl import \
    FeedbackRepositoryImplementation
from data_base.repository.user.user_repository_impl import \
    UserRepositoryImplementation
from keyboards.admin import keyboard_delete_update, keyboard_update_success

admin_update_feedback_router = Router()


@admin_update_feedback_router.callback_query(F.data.startswith("update_choice_"))
async def update_choice(callback: types.CallbackQuery):
    id_feedback = callback.data.split("_")[-1]
    keyboard_status = await keyboard_update_success(id_feedback)
    await callback.message.edit_reply_markup(reply_markup=keyboard_status)


@admin_update_feedback_router.callback_query(F.data.startswith("update_status_"))
async def update_status(callback: types.CallbackQuery):
    feedback_id = int(callback.data.split("_")[-1])
    status = callback.data.split("_")[-2]
    keyboard = await keyboard_delete_update(feedback_id)

    feedback = await FeedbackRepositoryImplementation.update_feedback_status(
        feedback_id=feedback_id, status=status
    )
    if feedback.user_id is not None:
        await UserRepositoryImplementation.update_user_status(
            user_id=feedback.user_id, status="available"
        )

    await callback.message.edit_text(
        text=f"Дата: {feedback.dateTimeFeedback.date()}\n"
        f"Время: {feedback.dateTimeFeedback.time()}\n"
        f"Статус: {feedback.status}\n"
        f"ID Пользователя: {feedback.user_id}\nПользователь: {feedback.username}",
        reply_markup=keyboard,
    )


@admin_update_feedback_router.callback_query(F.data.startswith("update_false_"))
async def update_status_cancel(callback: types.CallbackQuery):
    id_feedback = int(callback.data.split("_")[-1])
    keyboard = await keyboard_delete_update(id_feedback)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
