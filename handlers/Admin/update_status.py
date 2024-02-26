""""""

from aiogram import F, Router, types

from data_base.repository.feedback.feedback_repository_impl import \
    FeedbackRepositoryImplementation
from data_base.repository.user.user_repository_impl import \
    UserRepositoryImplementation
from data_base.shemas.user import UserDto
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

    feedback = await FeedbackRepositoryImplementation.get_feedback_by_id(
        feedback_id=feedback_id
    )
    updated_feedback = await FeedbackRepositoryImplementation.update_feedback_status(
        feedback_id=feedback_id, status=status, user_id=None, username=None
    )

    if user := await UserRepositoryImplementation.get_user_by_id(feedback.user_id):
        await UserRepositoryImplementation.update_user(
            user_dto=UserDto(
                id=user.id,
                username=user.username,
                fullname=user.fullname,
                status="available",
                id_feedback=None,
                dateTimeFeedback=None,
            )
        )

    await callback.message.edit_text(
        text=f"Дата: {updated_feedback.dateTimeFeedback.date()}\n"
        f"Время: {updated_feedback.dateTimeFeedback.time()}\n"
        f"Статус: {updated_feedback.status}\n"
        f"ID Пользователя: {updated_feedback.user_id}\nПользователь: {updated_feedback.username}",
        reply_markup=keyboard,
    )


@admin_update_feedback_router.callback_query(F.data.startswith("update_false_"))
async def update_status_cancel(callback: types.CallbackQuery):
    id_feedback = int(callback.data.split("_")[-1])
    keyboard = await keyboard_delete_update(id_feedback)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
