from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def edit_item_status_keyboard(old_status: str):
    if old_status == "available":
        new_status = "unavailable"
    else:
        new_status = "available"
    cb_data = new_status
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text=f"{new_status}",
                    callback_data=cb_data)
            ],
            [
                InlineKeyboardButton(
                    text="Отменить",
                    callback_data="Cancel_edit_item_parameter")
            ],
        ]
    )
    return markup
