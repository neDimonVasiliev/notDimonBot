from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirm_add_item_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Подтвердить",
                callback_data="Confirm_item")
        ],
        [
            InlineKeyboardButton(
                text="Отменить",
                callback_data="Cancel_add_item")
        ],
    ]
)