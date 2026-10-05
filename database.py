from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession)
from sqlalchemy.orm import DeclarativeBase
from config import settings
engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo = True
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
async_session = AsyncSessionLocal

class Base(DeclarativeBase):
    pass