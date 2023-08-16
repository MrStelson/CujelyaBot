from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("question", "Задать вопрос Кужеле"),
            types.BotCommand("resume", "Отправить резюме для разбора"),
            types.BotCommand("feedback", "Записаться на консультацию"),
        ]
    )
