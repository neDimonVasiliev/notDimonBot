from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

register_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="По объявлению",
                callback_data="Advertisement")
        ],
        [
            InlineKeyboardButton(
                text="Ввести вручную",
                callback_data="Enter_id_manually")
        ],
        [
            InlineKeyboardButton(
                text="Отмена",
                callback_data="Cancel_registration")
        ],
    ]
)

