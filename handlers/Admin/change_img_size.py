import os
import sys
from config import CHAT_ID
from aiogram import F, Router, types
from keyboards.admin import admin_main_keyboard
from keyboards.client import cancel_keyboard
from states.States import FSMChangeImgSize as ImgState
from loader import bot
from PIL import Image
from aiogram.types import FSInputFile, BufferedInputFile

admin_change_img_size = Router()


@admin_change_img_size.message(F.text == "Сжать изображение")
async def change_img_size_start(message: types.Message, state: ImgState):
    await state.set_state(ImgState.img_file)
    await message.answer(
        "Отправь изображение в виде файла", reply_markup=cancel_keyboard
    )


@admin_change_img_size.message(ImgState.img_file, F.text == "Отмена")
async def cancel_handler_img(message: types.Message, state: ImgState):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.reply("Отменено", reply_markup=admin_main_keyboard)


@admin_change_img_size.message(ImgState.img_file, F.content_type.in_({"document"}))
async def take_img_file(message: types.Message, state: ImgState):
    image_name = message.document.file_name
    image_id = message.document.file_id
    image = await bot.get_file(image_id)
    image_io = await bot.download_file(image.file_path)
    new_filename = f"./temp/{image_name}"

    start_size = sys.getsizeof(image_io)

    pillow_img = Image.open(image_io)
    pillow_img = pillow_img.convert(mode="P")
    pillow_img.save(new_filename)

    try:
        new_img_size = os.path.getsize(new_filename)

        if (quality := 57 * 1024 / new_img_size) < 1:
            pillow_img.save(new_filename, quality=quality * 100, optimize=True, mode="RGB")
            new_img_size = os.path.getsize(new_filename)

        new_image = FSInputFile(new_filename)

        await state.clear()
        await message.delete()
        await message.answer_document(
            document=new_image,
            caption=f"Фактический коэффициент сжатия: {new_img_size / start_size:.2f}\n"
            f"Вес файла: {new_img_size / 1024:.2f}Кб",
            reply_markup=admin_main_keyboard,
        )
    finally:
        os.remove(path=new_filename)
