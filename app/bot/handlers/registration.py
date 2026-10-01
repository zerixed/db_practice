from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from sqlalchemy.ext.asyncio import AsyncSession
from crud import get_user_by_tg_id, update_user_profile, upsert_user_profile
from app.bot.handlers.keyboards import get_profile, get_main_menu_keyboard
from html import escape
router = Router()
class EditProfile(StatesGroup):
    name=State()
    age=State()
    about=State()
class ProfileForm(StatesGroup):
    name=State()
    age=State()
    about=State()

@router.message(Command("start", "register"))
async def cmd_start(message:Message, state:FSMContext, session:AsyncSession):
    user = await get_user_by_tg_id(session, message.from_user.id)
    if user:
        text = (
            f"Glad to see u, <b>{user.name}</b>! \n"
            f"<b>Your profile:</b>\n"
            f"Name:{user.name}\n"
            f"age:{user.age}\n"
            f"bio:{user.about}"
        )
        await message.answer(
            text, parse_mode="HTML", reply_markup=get_profile()
        )
    else:
        await message.answer("Hi, create your profile. What is your name?")
        await state.set_state(ProfileForm.name)
@router.message(Command("profile"))
async def cmd_profile(message:Message,session:AsyncSession):
    user = await get_user_by_tg_id(session, message.from_user.id)
    if not user:
        await message.answer("Not registred yet. Write /start")
        return
    text = (
        f"<b>Your profile:</b>\n"
        f"Name:{user.name}\n"
        f"age:{user.age}\n"
        f"bio:{user.about}"
    )
    await message.answer(
        text, parse_mode="HTML", reply_markup=get_profile()
    )
@router.message(F.text == "My profile")
async def btn_profile(message: Message, session: AsyncSession):
    await cmd_profile(message, session)
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
    await upsert_user_profile(
        session,
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        name=data.get("name"),
        age=data.get("age"),
        about=message.text.strip(),
    )
    await state.clear()
    await message.answer("Profile was saved!Select action below:",
                         reply_markup=get_main_menu_keyboard())
@router.callback_query(F.data=="edit_name")
async def start_edit_name(callback:CallbackQuery, state: FSMContext):
    await callback.message.answer("Enter new name:")
    await state.set_state(EditProfile.name)
    await callback.answer()
@router.callback_query(F.data=="edit_age")
async def start_edit_age(callback:CallbackQuery, state:FSMContext):
    await callback.message.answer("enter new age:")
    await state.set_state(EditProfile.age)
    await callback.answer()
@router.callback_query(F.data=="edit_about")
async def start_edit_about(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer("Enter new bio:")
    await state.set_state(EditProfile.about)
    await callback.answer()
@router.message(EditProfile.name)
async def process_edit_name(message:Message, state: FSMContext, session: AsyncSession):
    new_name = message.text.strip()
    if len(new_name) > 50:
        await message.answer("Name so long. Try again (50 symbol max)")
        return
    await update_user_profile(session, message.from_user.id, name = new_name)
    await state.clear()
    await message.answer("Name updated")
@router.message(EditProfile.age)
async def process_edit_age(message:Message, state: FSMContext, session:AsyncSession):
    try:
        age = int(message.text)
    except ValueError:
        await message.answer("Enter age in numbers")
        return
    if not (10 <= age <= 100):
        await message.answer("Enter real age")
        return
    await update_user_profile(session, message.from_user.id, age = age)
    await state.clear()
    await message.answer("Age updated")
@router.message(EditProfile.about)
async def process_edit_about(message:Message, state:FSMContext, session: AsyncSession):
    new_about = message.text.strip()
    if len(new_about) > 300:
        await message.answer("Bio is too long (300 symbols max)")
        return
    await update_user_profile(session,message.from_user.id, about=new_about)
    await state.clear()
    await message.answer("Bio updated")