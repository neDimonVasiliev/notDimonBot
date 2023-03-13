from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

payment_method_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="PAYMASTER",
                callback_data="PAYMASTER_payment_method")
        ],
        [
            InlineKeyboardButton(
                text="Бонусы",
                callback_data="Bonus_payment_method")
        ],
        [
            InlineKeyboardButton(
                text="Отменить",
                callback_data="Cancel_buy_item")
        ],
    ]
)