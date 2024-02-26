from aiogram import types, Router, F

from data_base.repository.feedback.feedback_repository_impl import (
    FeedbackRepositoryImplementation,
)
from data_base.repository.user.user_repository_impl import UserRepositoryImplementation
from keyboards.admin import keyboard_delete_success, keyboard_delete_update
from data_base.shemas.user import UserDto

admin_delete_feedback_router = Router()


@admin_delete_feedback_router.callback_query(F.data.startswith("delete_choice_"))
async def delete_feedback(callback: types.CallbackQuery):
    id_feedback = callback.data.split("_")[-1]
    keyboard_success = await keyboard_delete_success(id_feedback)
    await callback.message.edit_reply_markup(reply_markup=keyboard_success)


@admin_delete_feedback_router.callback_query(F.data.startswith("delete_true_"))
async def delete_feedback_success(callback: types.CallbackQuery):
    id_feedback = callback.data.split("_")[-1]

    feedback = await FeedbackRepositoryImplementation.delete_feedback(
        feedback_id=int(id_feedback)
    )
    if (
        user := await UserRepositoryImplementation.get_user_by_id(feedback.user_id)
    ) and user.status is not None:
        await UserRepositoryImplementation.update_user(
            user_dto=UserDto(
                id=feedback.user_id,
                username=user.username,
                fullname=user.fullname,
                status="available",
                id_feedback=None,
                dateTimeFeedback=None,
            )
        )

    await callback.message.edit_text("Запись удалена")


@admin_delete_feedback_router.callback_query(F.data.startswith("delete_false_"))
async def delete_feedback_cancel(callback: types.CallbackQuery):
    id_feedback = callback.data.split("_")[-1]
    keyboard = await keyboard_delete_update(int(id_feedback))
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@admin_delete_feedback_router.message(F.text.startswith("Удалить прошедшие записи"))
async def delete_all_last_feedback(message: types.message):
    await FeedbackRepositoryImplementation.delete_last_feedbacks()
    await message.answer(text="Прошедшие даты удалены")
