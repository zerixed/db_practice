from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from database import Base, engine, async_session
async def create_user(session: AsyncSession, name:str, phone:str):
    new_user = User(name=name, phone=phone)
    session.add(new_user)
    await session.commit()
    return new_user
async def get_users_by_name(session: AsyncSession, name:str):
    stmt = select(User).where(User.name == name)
    result = await session.execute(stmt)
    return result.scalars().all()
async def update_user_phone(session: AsyncSession, name:str, new_phone:str):
    stmt = update(User).where(User.name == name,).values(phone=new_phone)
    await session.execute(stmt)
    await session.commit()
async def delete_user(session:AsyncSession, name:str):
    stmt = delete(User).where(User.name == name)
    await session.execute(stmt)
    await session.commit()