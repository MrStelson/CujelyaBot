
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

Base_model = declarative_base()

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async_engine = create_async_engine(
    url=DATABASE_URL,
    # echo=True,
)
async_session_factory = async_sessionmaker(async_engine)
