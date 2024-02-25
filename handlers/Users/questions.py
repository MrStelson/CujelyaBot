from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.client import main_keyboard, cancel_keyboard, question_keyboard
from config import CHAT_ID
from states.States import FSMQuestion
from loader import bot

user_questions_router = Router()


@user_questions_router.message(Command("question"))
@user_questions_router.message(F.text == "Задать вопрос")
async def take_question(message: Message, state: FSMQuestion) -> None:
    await state.set_state(FSMQuestion.question)
    await message.reply(
        "Какой у тебя вопрос?\nДля отмены нажми кнопку или введи \n/cancel_question",
        reply_markup=cancel_keyboard,
    )


# exit FSMQuestion
@user_questions_router.message(FSMQuestion.question, F.text == "Отмена")
@user_questions_router.message(FSMQuestion.question, Command("cancel_question"))
async def cancel_handler_question(message: Message, state: FSMQuestion) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.reply("Твой вопрос отменен", reply_markup=main_keyboard)


@user_questions_router.message(FSMQuestion.question)
async def give_question(message: Message, state: FSMQuestion) -> None:
    await state.update_data(user_question=message.text, username=message.from_user.username)
    await message.answer(text='Отправить?', reply_markup=question_keyboard)


@user_questions_router.callback_query(FSMQuestion.question, F.data == 'question_false')
async def cancel_handler_question_callback(callback: CallbackQuery, state: FSMQuestion):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("Твой вопрос отменен", reply_markup=main_keyboard)
    await callback.answer()


@user_questions_router.callback_query(FSMQuestion.question, F.data == 'question_true')
async def send_question(callback: CallbackQuery, state: FSMQuestion):
    data = await state.get_data()
    question = data['user_question']
    username = data.get('username')
    await bot.send_message(CHAT_ID, text=f'❓❓❓\n{question}\n❓❓❓\nfrom @{username}')
    await callback.answer('Отправлено')
    await callback.message.delete()
    await callback.message.answer(text='Твой вопрос задан!\nОтвечу в канале🐝', reply_markup=main_keyboard)
    await state.clear()
