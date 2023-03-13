from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from data.config import admins
from keyboards.inline.menu.admin.edit_item_keyboard import finish_edit_item_cd

continue_edit_item_cd = CallbackData("continue_edit_item", "item_id")

async def continue_edit_item_keyboard(item_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Продолжить",
                    callback_data=continue_edit_item_cd.new(item_id=item_id))
            ],
            [
                InlineKeyboardButton(
                    text="Закончить редактирование",
                    callback_data=finish_edit_item_cd.new(item_id=item_id))
            ],
        ]
    )

    return markup
