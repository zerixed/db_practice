from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from crud import get_or_create_user
user = Router()
@user.message(CommandStart())
async def cmd_start(message:Message, session: AsyncSession):
    new_user = await get_or_create_user(
        session=session,
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )
    await message.answer(
        f"Hello, {new_user.first_name}!\n\n"
        f"You are successfully created in db PostgreSQL!\n"
        f"Your id in db: {new_user.id}"
    )