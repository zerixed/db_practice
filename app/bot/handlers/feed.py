import logging
from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from contextlib import suppress
from sqlalchemy.ext.asyncio import AsyncSession
from crud import get_random_candidate, save_reaction, get_user_by_tg_id, reset_user_reactions
from app.bot.handlers.keyboards import get_matching_keyboard, get_reset_keyboard, get_like_notification_keyboard
logger = logging.getLogger(__name__)
router = Router()
async def get_specific_candidate_card(session:AsyncSession, candidate_id:int):
    candidate = await get_user_by_tg_id(session, candidate_id)
    if not candidate:
        return "profile not available yet", None
    text = f"<b>{candidate.name}</b>,{candidate.age}\n<i>{candidate.about}</i>"
    kb = get_matching_keyboard(candidate.telegram_id)
    return text, kb
async def get_candidate_card(session:AsyncSession, user_id: int):
    candidate = await get_random_candidate(session, user_id)
    if not candidate:
        return "No profile aviables to view", get_reset_keyboard()
    text = f"<b>{candidate.name}</b>, {candidate.age}\n<i>{candidate.about}</i>"
    kb = get_matching_keyboard(candidate.telegram_id)
    return text, kb
@router.message(Command("search"))
async def cmd_search(message:Message, session:AsyncSession):
    text, kb = await get_candidate_card(session, message.from_user.id)
    await message.answer(text, parse_mode="HTML", reply_markup=kb)
async def render_next_candidate(callback: CallbackQuery, session:AsyncSession):
    text, kb = await get_candidate_card(session, callback.from_user.id)
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb)
@router.callback_query(F.data == "reset_reactions")
async def process_reset(callback:CallbackQuery, session:AsyncSession):
    await reset_user_reactions(session, callback.from_user.id)
    await callback.answer("Watch history cleared")
    await render_next_candidate(callback,session)
@router.callback_query(F.data.startswith("show_card_"))
async def process_show_card(callback:CallbackQuery,session:AsyncSession):
    await callback.answer()
    liker_id = int(callback.data.split("_")[2])
    text, kb = await get_specific_candidate_card(session, liker_id)
    await callback.message.answer(text, parse_mode="HTML", reply_markup=kb)
@router.message(F.text == "View profiles")
async def btn_search(message: Message, session: AsyncSession):
    await cmd_search(message, session)
@router.callback_query(F.data.startswith("like_"))
async def process_like(callback: CallbackQuery, session:AsyncSession, bot:Bot):
    target_id = int(callback.data.split("_")[1])
    current_user_id = callback.from_user.id
    is_match = await save_reaction(
        session,
        from_id=current_user_id,
        to_id=target_id,
        is_like=True,
    )
    await callback.answer("Like")
    if is_match:
        current_user = await get_user_by_tg_id(session, current_user_id)
        target_user = await get_user_by_tg_id(session, target_id)
        target_link = (
            f"@{target_user.username}"
            if target_user.username
            else f"<a href='tg://user?id={target_id}'>{target_user.name}</a>"
        )
        current_link = (
            f"@{current_user.username}"
            if current_user.username
            else f"<a href='tg://user?id={current_user_id}'>{current_user.name}</a>"
        )
        await callback.message.answer(
            f"<b>Match</b>\n"
            f"u liked <b> {target_user.name}</b>, it was mutually\n"
            f"contact: {target_link}",
            parse_mode="HTML",
        )
        try:
            await bot.send_message(
                chat_id=target_id,
                text=(
                    f"<b>Match</b>\n"
                    f"u liked <b> {current_user.name}</b>, it was mutually\n"
                    f"contact: {current_link}"
                ),
                parse_mode="HTML",
            )
        except Exception as e:
            logger.error(f"Could not notify user of the match {target_id}: {e}")
    else:
        try:
            await bot.send_message(
                chat_id=target_id,
                text=(
                    "<b>someone liked your profile</b>\n"
                    "Press button bellow, to match back"
                ),
                parse_mode="HTML",
                reply_markup=get_like_notification_keyboard(current_user_id),
            )
            logger.info(f"like notification successfully sent to user {target_id}")
        except Exception as e:
            logger.error(f"Could not notify user of the matc {target_id}: {e}")
    await render_next_candidate(callback, session)
@router.callback_query(F.data.startswith("dislike_"))
async def process_skip(callback: CallbackQuery, session:AsyncSession):
    target_id= int (callback.data.split("_")[1])
    await save_reaction(
        session,
        from_id=callback.from_user.id,
        to_id=target_id,
        is_like=False
    )
    await callback.answer("skip")
    await render_next_candidate(callback,session)
@router.callback_query(F.data=="open_feed")
async def process_open_feed(callback:CallbackQuery, session:AsyncSession):
    await callback.answer()
    text, kb = await get_candidate_card(session, callback.from_user.id)
    await callback.message.answer(text, parse_mode="HTML", reply_markup=kb)