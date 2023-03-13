from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

cancel_buy_item_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Отменить",
                callback_data="Cancel_buy_item")
        ],
    ]
)
