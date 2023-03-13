from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirm_delivery_address_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Подтвердить",
                callback_data="Confirm_delivery_address")
        ],
        [
            InlineKeyboardButton(
                text="Исправить",
                callback_data="Edit_delivery_address")
        ],
        [
            InlineKeyboardButton(
                text="Отменить",
                callback_data="Cancel_buy_item")
        ],
    ]
)
