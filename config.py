import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")

ADMIN_ID_FIRST = int(os.getenv("ADMIN_ID_FIRST"))
ADMIN_ID_SECOND = int(os.getenv("ADMIN_ID_SECOND"))
CHAT_ID = int(os.getenv("CHAT_ID"))
HOUR_OFFSET = int(os.getenv("HOUR_OFFSET"))
YEAR = int(os.getenv("YEAR"))

# Список администраторов
ADMIN_ID_LIST = [ADMIN_ID_FIRST, ADMIN_ID_SECOND]
