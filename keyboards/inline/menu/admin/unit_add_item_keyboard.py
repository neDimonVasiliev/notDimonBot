from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

unit_add_item_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="кг.",
                callback_data="unit_kilo")
        ],
        [
            InlineKeyboardButton(
                text="г.",
                callback_data="unit_gram")
        ],
        [
            InlineKeyboardButton(
                text="шт.",
                callback_data="unit_piece")
        ],
        [
            InlineKeyboardButton(
                text="л.",
                callback_data="unit_liter")
        ],
        [
            InlineKeyboardButton(
                text="уп.",
                callback_data="unit_package")
        ],
        [
            InlineKeyboardButton(
                text="Отменить",
                callback_data="Cancel_add_item")
        ],
    ]
)
