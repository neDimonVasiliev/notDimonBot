from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def start_item_keyboard_data(item_id):
    item_id = item_id
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text="Показать товар",
                                     url=f"https://t.me/notdimonbot?start=item_id-{item_id}")
            ],
        ]
    )
    print("Внутри функции формирования клавиатуры start_item")
    return markup
