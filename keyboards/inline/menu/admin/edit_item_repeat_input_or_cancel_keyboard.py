# этот файл требует глубокой переработки

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.menu.admin.edit_item_keyboard import edit_item_photo_cd, edit_item_price_cd, \
    edit_item_stock_quantity_cd

callback_data_dict = {"edit_item_price": edit_item_price_cd,
                      "edit_item_photo": edit_item_photo_cd,
                      "edit_item_stock_quantity": edit_item_stock_quantity_cd}

async def edit_item_repeat_input_or_cancel_keyboard(item_id, parameter):
    callback_data = callback_data_dict[parameter]
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Повторить ввод",
                    callback_data=callback_data.new(item_id=item_id))
            ],
            [
                InlineKeyboardButton(
                    text="Отменить",
                    callback_data="Cancel_edit_item_parameter")
            ],
        ]
    )
    return markup