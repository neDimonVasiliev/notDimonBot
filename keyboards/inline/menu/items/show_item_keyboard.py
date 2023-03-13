from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from data.config import admins

buy_item_cd = CallbackData("buy_item", "item_id")
edit_item_cd = CallbackData("edit_item", "item_id")


async def show_item_keyboard_data(item_id, telegram_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text="Купить",
                    callback_data=buy_item_cd.new(item_id=item_id))
            ],
        ]
    )
    if telegram_id in admins:
        order_button = InlineKeyboardButton(
            text=f"Редактировать товар",
            callback_data=edit_item_cd.new(item_id=item_id))
        markup.row(order_button)
    markup.row(InlineKeyboardButton(
                    text="Отменить",
                    callback_data="Cancel_buy_item"))
    print("Внутри функции формирования клавиатуры")
    return markup
