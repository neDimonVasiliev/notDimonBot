from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu_admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Добавить товар",
                callback_data="Add_item")
        ],
        # [
        #     InlineKeyboardButton(
        #         text="Пользователи",
        #         callback_data="Users")
        # ],
        [
            InlineKeyboardButton(
                text="Каталог",
                switch_inline_query_current_chat=""
            )
        ],
    ]
)