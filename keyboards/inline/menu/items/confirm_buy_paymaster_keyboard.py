from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirm_buy_item_paymaster_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Подтвердить заказ",
                callback_data="Confirm_buy_item_paymaster")
        ],
        [
            InlineKeyboardButton(
                text="Отменить",
                callback_data="Cancel_buy_item")
        ],
    ]
)
