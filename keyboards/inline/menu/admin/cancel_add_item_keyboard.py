from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

cancel_add_item_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Отменить",
                callback_data="Cancel_add_item")
        ],
    ]
)
