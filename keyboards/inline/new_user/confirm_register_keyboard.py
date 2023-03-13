from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.utils.callback_data import CallbackData

confirm_register_cd = CallbackData("Confirm_registration", "referral_id")


async def confirm_register_keyboard_data(referral_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Подтвердить",
                    callback_data=confirm_register_cd.new(referral_id=referral_id))
            ],
            [
                InlineKeyboardButton(
                    text="Отменить",
                    callback_data="Cancel_registration")
            ],
        ]
    )
    print("Внутри функции формирования клавиатуры")
    return markup
