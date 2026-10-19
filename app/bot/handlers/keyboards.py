from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
def get_profile() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="edit name", callback_data="edit_name"),
                InlineKeyboardButton(text="edit age", callback_data="edit_age"),
            ],
            [
                InlineKeyboardButton(text="edit gender", callback_data="edit_gender"),
                InlineKeyboardButton(text="edit photo", callback_data="edit_photo"),
            ],
            [
                InlineKeyboardButton(text="edit about", callback_data="edit_about"),
                InlineKeyboardButton(text="edit target gender", callback_data="edit_target_gender")
            ],
        ]
    )
def get_matching_keyboard(target_user_id: int) -> InlineKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Skip"),
                KeyboardButton(text="Like"),
                KeyboardButton(text="Finish")
            ]
        ],
        resize_keyboard=True,
    )
def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="View profiles")],
            [KeyboardButton(text="My profile")],
        ],
        resize_keyboard=True,
    )
def get_reset_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="View profiles again"),
                KeyboardButton(text="My profile")
                ]
            ],
        resize_keyboard=True,
    )
def get_like_notification_keyboard(liker_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="view profiles", callback_data=f"show_card_{liker_id}")]
        ]
    )
def get_gender_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Man"), KeyboardButton(text="Woman")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
def get_skip_bio_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="skip")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
def get_target_gender_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Men"), KeyboardButton(text="Women")],
            [KeyboardButton(text="Everyone")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )