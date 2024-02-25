from aiogram import Bot, types

from config import BOT_TOKEN
from utils import BotUtils

TOKEN = BOT_TOKEN
bot = Bot(token=TOKEN)


async def on_startup():
    print("CujelyaBot online")
    await bot.set_my_commands(
        commands=BotUtils.start_commands, scope=types.BotCommandScopeAllPrivateChats()
    )
