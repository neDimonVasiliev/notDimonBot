from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirm_buy_item_balance_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Подтвердить заказ",
                callback_data="Confirm_buy_item_balance")
        ],
        [
            InlineKeyboardButton(
                text="Отменить",
                callback_data="Cancel_buy_item")
        ],
    ]
)