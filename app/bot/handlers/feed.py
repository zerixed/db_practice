import logging

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from crud import get_random_candidate, save_reaction, get_user_by_tg_id, reset_user_reactions
from app.bot.handlers.keyboards import get_matching_keyboard, get_reset_keyboard, get_like_notification_keyboard, get_main_menu_keyboard
logger = logging.getLogger(__name__)
router = Router()
class FeedStates(StatesGroup):
    browsing = State()
async def format_candidate_card(candidate) -> str:
    age_str = f", {candidate.age}" if candidate.age else""
    about_str =f"\n<i>{candidate.about}</i>"if candidate.about else""
    return f"<b>{candidate.name}</b>{age_str}{about_str}"
async def get_specific_candidate_card(session:AsyncSession, candidate_id:int):
    candidate = await get_user_by_tg_id(session, candidate_id)
    if not candidate:
        return "profile not available yet", None, None
    text = f"<b>{candidate.name}</b>,{candidate.age}\n<i>{candidate.about}</i>"
    kb = get_matching_keyboard(candidate.telegram_id)
    return text, kb, candidate.photo_id
async def get_candidate_card(session:AsyncSession, user_id: int):
    candidate = await get_random_candidate(session, user_id)
    if not candidate:
        return "No profile aviables to view", get_reset_keyboard(), None
    text = f"<b>{candidate.name}</b>, {candidate.age}\n<i>{candidate.about}</i>"
    kb = get_matching_keyboard(candidate.telegram_id)
    return text, kb, candidate.photo_id
async def render_next_candidate(message:Message, session:AsyncSession, state:FSMContext, user_id:int):
    candidate = await get_random_candidate(session, user_id)
    if not candidate:
        await state.clear()
        return await message.answer(
            "You've run out of profiles! Click below to reset your history",
            reply_markup=get_reset_keyboard(),
        )
    await state.update_data(target_id=candidate.telegram_id)
    await state.set_state(FeedStates.browsing)
    text = await format_candidate_card(candidate)
    kb = get_matching_keyboard(candidate.telegram_id)
    if candidate.photo_id:
        await message.answer_photo(
            photo=candidate.photo_id,caption=text,parse_mode="HTML", reply_markup=kb
        )
    else:
        await message.answer(text, parse_mode="HTML", reply_markup=kb)
@router.message(Command("search"))
@router.message(F.text == "View profiles")
@router.message(F.text == "View profiles again")
async def btn_search(message: Message, session: AsyncSession, state:FSMContext):
    if message.text == "View profiles again":
        await reset_user_reactions(session,message.from_user.id)
    await render_next_candidate(message, session, state, message.from_user.id)
@router.message(FeedStates.browsing, F.text == ("Like"))
async def process_like(message:Message, session:AsyncSession,state:FSMContext, bot:Bot):
    data = await state.get_data()
    target_id = data.get("target_id")
    if not target_id:
        return await render_next_candidate(message, session, state, message.from_user.id)
    current_user_id = message.from_user.id
    is_match = await save_reaction(
        session,
        from_id=current_user_id,
        to_id=target_id,
        is_like=True,
    )
    if is_match:
        current_user = await get_user_by_tg_id(session, current_user_id)
        target_user = await get_user_by_tg_id(session, target_id)
        target_name = target_user.name if target_user else "User"
        current_name = current_user.name if current_user else "User"
        target_link = (
            f"@{target_user.username}"
            if target_user and target_user.username
            else f"<a href='tg://user?id={target_id}'>{target_name}</a>"
        )
        current_link = (
            f"@{current_user.username}"
            if current_user and current_user.username
            else f"<a href='tg://user?id={current_user_id}'>{current_name}</a>"
        )
        await message.answer(
            f"<b>Mutual like!</b>\n"
            f"<b>{target_name}</b> like you\n"
            f"contacts: {target_link}",
            parse_mode="HTML",
        )
        try:
            await bot.send_message(
                chat_id=target_id,
                text=(
                    f"<b>Mutual like!</b>\n"
                    f"<b>{current_name}</b> like you\n"
                    f"contacts: {current_link}"
                ),
                parse_mode="HTML",
            )
        except (TelegramForbiddenError, TelegramBadRequest) as e:
            logger.warning(f"Unable to notify user of a match {target_id}: {e}")
        except Exception as e:
            logger.error(f"Failed to send match to user{target_id}: {e}")
    else:
        try:
            await bot.send_message(
                chat_id=target_id,
                text=(
                    "<b>someone liked you!</b>\n"
                    "press button below to view profile."
                ),
                parse_mode="HTML",
                reply_markup=get_like_notification_keyboard(current_user_id),
            )
        except (TelegramForbiddenError, TelegramBadRequest) as e:
            logger.warning(f"Unable to notify user of a match{target_id}: {e}")
        except Exception as e:
            logger.error(f"Failed to send match to user {target_id}: {e}")
    await render_next_candidate(message, session, state, message.from_user.id)
@router.message(FeedStates.browsing, F.text == ("Skip"))
async def process_skip(message: Message, session:AsyncSession, state:FSMContext):
    data = await state.get_data()
    target_id = data.get("target_id")
    if target_id:
        await save_reaction(
        session,
        from_id=message.from_user.id,
        to_id=target_id,
        is_like=False
    )
    await render_next_candidate(message,session, state, message.from_user.id)
@router.message(FeedStates.browsing,F.text == "Finish")
async def process_stop_feed(message:Message, state:FSMContext):
    await state.clear()
    await message.answer(
        "Profile viewing is paused.",
        reply_markup=get_main_menu_keyboard(),
    )
@router.callback_query(F.data=="open_feed")
async def process_open_feed(callback:CallbackQuery, session:AsyncSession, state:FSMContext):
    await callback.answer()
    await render_next_candidate(callback.message,session,state,callback.from_user.id)
@router.callback_query(F.data == "reset_reactions")
async def process_reset(callback:CallbackQuery, session:AsyncSession, state:FSMContext):
    await reset_user_reactions(session, callback.from_user.id)
    await callback.answer("Watch history cleared")
    try:
        await callback.message.delete()
    except Exception:
        pass
    await render_next_candidate(callback.message,session,state, callback.from_user.id)
@router.callback_query(F.data.startswith("show_card_"))
async def process_show_card(callback:CallbackQuery,session:AsyncSession, state:FSMContext):
    await callback.answer()
    liker_id = int(callback.data.split("_")[-1])
    await state.update_data(target_id=liker_id)
    await state.set_state(FeedStates.browsing)
    text, kb, photo_id = await get_specific_candidate_card(session, liker_id)
    if photo_id:
        await callback.message.answer_photo(photo=photo_id,caption=text,parse_mode="HTML", reply_markup=kb)
    else:
        await callback.message.answer(text, parse_mode="HTML", reply_markup=kb)
@router.message(F.text.in_({"Like", "Skip", "Finish"}))
async def process_feed_fallback(message:Message,session:AsyncSession, state:FSMContext):
    if message.text == "Finish":
        await state.clear()
        return await message.answer(
            "profile viewing is paused.",
            reply_markup=get_main_menu_keyboard(),
        )
    await render_next_candidate(message, session, state, message.from_user.id)