from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
def get_profile() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="edit name", callback_data="edit_name"),
                InlineKeyboardButton(text="edit age", callback_data="edit_age"),
                InlineKeyboardButton(text="edit bio", callback_data="edit_about"),
            ]
        ]
    )
def get_matching_keyboard(target_user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Skip_", callback_data=f"dislike_{target_user_id}"),
                InlineKeyboardButton(text="Like_", callback_data=f"like_{target_user_id}"),
            ]
        ]
    )
def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="View profiles")],
            [KeyboardButton(text="My profile")],
        ],
        resize_keyboard=True,
    )
def get_reset_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="View profiles again", callback_data="reset_reactions")]
        ]
    )
def get_like_notification_keyboard(liker_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="view profiles", callback_data=f"show_card_{liker_id}")]
        ]
    )