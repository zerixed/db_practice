from sqlalchemy import select, delete, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Reaction
from typing import Optional
from sqlalchemy.dialects.postgresql import insert
async def get_or_create_user(
        session: AsyncSession,
        telegram_id: int,
        username: Optional[str] = None,
        name: Optional[str] = None,
        ) -> User:
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if not user:
        user = User(
            telegram_id = telegram_id,
            username = username,
            name = name,
        )  
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user
async def update_user_username(
        session: AsyncSession, telegram_id:int, new_username:str
        ):
    stmt = (
        update(User)
        .where(User.telegram_id == telegram_id)
        .values(username=new_username)
    )
    await session.execute(stmt)
    await session.commit()
async def delete_user(session:AsyncSession, telegram_id:int):
    stmt = delete(User).where(User.telegram_id == telegram_id)
    await session.execute(stmt)
    await session.commit()
async def get_user_by_tg_id(session:AsyncSession, telegram_id:int) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
async def update_user_profile(session:AsyncSession, telegram_id:int, **kwargs):
    stmt = (
        update(User)
        .where(User.telegram_id == telegram_id)
        .values(**kwargs)
    )
    await session.execute(stmt)
    await session.commit()
async def upsert_user_profile(
        session:AsyncSession,
        telegram_id: int,
        username: str | None,
        name: str,
        age: int,
        gender:str,
        about: str,
        photo_id: str | None = None,
) -> None:
    stmt = (
        insert(User)
        .values(
            telegram_id=telegram_id,
            username=username,
            name=name,
            age=age,
            gender=gender,
            about=about,
            photo_id=photo_id,
        )
        .on_conflict_do_update(
            index_elements=["telegram_id"],
            set_={
                "username": username,
                "name": name,
                "age": age,
                "gender": gender,
                "about": about,
                "photo_id": photo_id,
            },
        )
    )
    await session.execute(stmt)
    await session.commit()
async def get_random_candidate(session:AsyncSession, user_id:int):
    evaluated_users = select(Reaction.to_user_id).where(
        Reaction.from_user_id == user_id
    )
    stmt = (
        select(User)
        .where(
            User.telegram_id != user_id,
            User.telegram_id.not_in(evaluated_users))
        .order_by(func.random())
        .limit(1)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
async def save_reaction(
        session:AsyncSession, from_id:int, to_id:int, is_like:bool
) -> bool:
    reaction = Reaction(
        from_user_id=from_id,
        to_user_id=to_id,
        is_like=is_like,
    )
    session.add(reaction)
    await session.commit()
    stmt = select(Reaction).where(
        Reaction.from_user_id == to_id,
        Reaction.to_user_id == from_id,
        Reaction.is_like == True,
    )
    result = await session.execute(stmt)
    has_mutual_like = result.scalars().first() is not None
    return has_mutual_like
async def reset_user_reactions(session:AsyncSession, user_id:int):
    stmt = delete(Reaction).where(
        (Reaction.from_user_id == user_id) | (Reaction.to_user_id == user_id)
    )
    await session.execute(stmt)
    await session.commit()