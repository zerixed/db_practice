from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from typing import Optional
async def get_or_create_user(
        session: AsyncSession,
        telegram_id: str,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        ) -> User:
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if not user:
        user = User(
            telegram_id = telegram_id,
            username = username,
            first_name = first_name,
        )  
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user
async def get_user_by_telegram_id(
        session: AsyncSession, telegram_id: int
        ) -> Optional[User]:
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    return result.scalars().first()
async def update_user_username(
        session: AsyncSession, telegram_id:int, new_username:int
        ):
    stmt = (
        update(User)
        .where(User.telegram_id == telegram_id)
        .values(username=new_username)
    )
    await session.execute(stmt)
    await session.commit
async def delete_user(session:AsyncSession, telegram_id:int):
    stmt = delete(User).where(User.telegram_id == telegram_id)
    await session.execute(stmt)
    await session.commit()  