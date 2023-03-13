from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

confirm_edit_item_name_cd = CallbackData("confirm_edit_item_name", "item_id")
confirm_edit_item_description_cd = CallbackData("confirm_edit_item_description", "item_id")
confirm_edit_item_photo_cd = CallbackData("confirm_edit_item_photo", "item_id")
confirm_edit_item_price_cd = CallbackData("confirm_edit_item_price", "item_id")
confirm_edit_item_stock_quantity_cd = CallbackData("confirm_edit_item_stock_quantity", "item_id")
confirm_edit_item_unit_cd = CallbackData("confirm_edit_item_unit", "item_id")
confirm_edit_item_status_cd = CallbackData("confirm_edit_item_status", "item_id")

callback_data_dict = {"edit_item_name": confirm_edit_item_name_cd,
                      "edit_item_description": confirm_edit_item_description_cd,
                      "edit_item_photo": confirm_edit_item_photo_cd,
                      "edit_item_price": confirm_edit_item_price_cd,
                      "edit_item_stock_quantity": confirm_edit_item_stock_quantity_cd,
                      "edit_item_unit": confirm_edit_item_unit_cd,
                      "edit_item_status": confirm_edit_item_status_cd}

async def confirm_edit_item_parameter_keyboard(item_id, parameter):
    callback_data = callback_data_dict[parameter]
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Подтвердить",
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

