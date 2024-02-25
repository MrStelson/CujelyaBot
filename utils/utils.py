from aiogram.types import BotCommand


class BotUtils:

    start_commands = [
        BotCommand(command='start', description="Запустить бота"),
        BotCommand(command='question', description="Задать вопрос Кужеле"),
        BotCommand(command='resume', description="Отправить резюме для разбора"),
        BotCommand(command='feedback', description="Записаться на консультацию"),
        BotCommand(command='help', description="Помощь"),
    ]
