import os

from aiogram import types
from aiogram.dispatcher.filters.builtin import Command, Text
from dotenv import load_dotenv, find_dotenv

from loader import dp, bot
from keyboards.client import mainKeyboard, cancelKeyboard
from config import CHAT_ID
from states.States import FSMQuestion

load_dotenv(find_dotenv())


@dp.message_handler(text='Задать вопрос', state=None)
@dp.message_handler(Command('question'), state=None)
async def take_question(message: types.message):
    await FSMQuestion.question.set()
    await message.reply('Какой у тебя вопрос?\nДля отмены нажми кнопку или введи \n/cancel_question',
                        reply_markup=cancelKeyboard)


# exit FSMQuestion
@dp.message_handler(text='Отмена', state=FSMQuestion.question)
@dp.message_handler(state=FSMQuestion.question, commands='cancel_question')
async def cancel_handler_question(message: types.message, state: FSMQuestion):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Твой вопрос отменен", reply_markup=mainKeyboard)


@dp.message_handler(state=FSMQuestion.question)
async def give_question(message: types.message, state: FSMQuestion):
    question = message.text
    await bot.send_message(CHAT_ID, text=f'{question}\nfrom @{message.from_user.username}')
    await message.answer(text='Твой вопрос задан!', reply_markup=mainKeyboard)
    await state.finish()
