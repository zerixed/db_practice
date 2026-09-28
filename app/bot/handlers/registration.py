from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F, Router
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from sqlalchemy.dialects.postgresql import insert
router = Router()
class ProfileForm(StatesGroup):
    name=State()
    age=State()
    about=State()

@router.message(Command("register"))
async def reg(message:Message, state:FSMContext):
    await state.set_state(ProfileForm.name)
    await message.answer("Enter your name")
@router.message(ProfileForm.name)
async def process_name(message:Message, state:FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ProfileForm.age)
    await message.answer("Enter your age")
@router.message(ProfileForm.age)
async def process_age(message:Message, state:FSMContext):
    try:
        age = int(message.text)
    except ValueError:
        await message.answer("Enter your age in  numbers")
        return
    if not (10 <= age <= 100):
        await message.answer("Enter your real age")
        return
    await state.update_data(age=age)
    await state.set_state(ProfileForm.about)
    await message.answer("tell something about yourself")
@router.message(ProfileForm.about)
async def process_about(message:Message, state:FSMContext, session:AsyncSession):
    data = await state.get_data()
    stmt = (
        insert(User)
        .values(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            name=data.get("name"),
            age=data.get("age"),
            about=message.text,
        )
        .on_conflict_do_update(
            index_elements=["telegram_id"],
            set_={
                "username":message.from_user.username,
                "name":data.get("name"),
                "age":data.get("age"),
                "about":message.text,
            }
        )
    )
    await session.execute(stmt)
    await session.commit()
    await state.clear()
    await message.answer("Profile was saved")