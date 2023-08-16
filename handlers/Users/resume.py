import os

from aiogram import types
from aiogram.dispatcher.filters.builtin import Command, Text
from dotenv import load_dotenv, find_dotenv

from loader import dp, bot
from keyboards.client import mainKeyboard, cancelKeyboard

from states.States import FSMResume

load_dotenv(find_dotenv())


@dp.message_handler(text='Отправить резюме на разбор', state=None)
@dp.message_handler(Command('resume'), state=None)
async def take_resume(message: types.Message):
    await FSMResume.resume.set()
    await message.reply('Отправь резюме в формате .pdf\nДля отмены нажми кнопку или введи \n/cancel_resume',
                        reply_markup=cancelKeyboard)


# exit FSMQuestion
@dp.message_handler(text='Отмена', state=FSMResume.resume)
@dp.message_handler(state=FSMResume.resume, commands='cancel_resume')
async def cancel_handler_resume(message: types.Message, state: FSMResume):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Твое резюме не отправлено", reply_markup=mainKeyboard)


@dp.message_handler(content_types=[types.ContentType.DOCUMENT], state=FSMResume.resume)
async def give_resume(message: types.Message, state: FSMResume):
    async with state.proxy() as data:
        data['resume_id'] = message.document.file_id
    await bot.send_document(os.getenv('CHAT_ID'), document=message.document.file_id)
    await bot.send_message(os.getenv('CHAT_ID'), text=f'Резюме from @{message.from_user.username}')
    await message.answer(text='Твое резюме отправлено', reply_markup=mainKeyboard)
    await state.finish()
