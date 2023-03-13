from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from data.config import admins

edit_item_name_cd = CallbackData("edit_item_name", "item_id")
edit_item_description_cd = CallbackData("edit_item_description", "item_id")
edit_item_photo_cd = CallbackData("edit_item_photo", "item_id")
edit_item_price_cd = CallbackData("edit_item_price", "item_id")
edit_item_stock_quantity_cd = CallbackData("edit_item_stock_quantity", "item_id")
edit_item_unit_cd = CallbackData("edit_item_unit", "item_id")
edit_item_status_cd = CallbackData("edit_item_status", "item_id")
finish_edit_item_cd = CallbackData("finish_edit_item", "item_id")


async def edit_item_keyboard_data(item_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Изменить наименование",
                    callback_data=edit_item_name_cd.new(item_id=item_id))
            ],
            [
                InlineKeyboardButton(
                    text="Изменить описание",
                    callback_data=edit_item_description_cd.new(item_id=item_id))
            ],
            [
                InlineKeyboardButton(
                    text="Изменить фото",
                    callback_data=edit_item_photo_cd.new(item_id=item_id))
            ],
            [
                InlineKeyboardButton(
                    text="Изменить стоимость",
                    callback_data=edit_item_price_cd.new(item_id=item_id))
            ],
            [
                InlineKeyboardButton(
                    text="Изменить количество на складе",
                    callback_data=edit_item_stock_quantity_cd.new(item_id=item_id))
            ],
            [
                InlineKeyboardButton(
                    text="Изменить единицы измерения товара",
                    callback_data=edit_item_unit_cd.new(item_id=item_id))
            ],
            [
                InlineKeyboardButton(
                    text="Изменить статус товара",
                    callback_data=edit_item_status_cd.new(item_id=item_id))
            ],
            [
                InlineKeyboardButton(
                    text="Закончить редактирование",
                    callback_data=finish_edit_item_cd.new(item_id=item_id))
            ],
        ]
    )

    return markup
