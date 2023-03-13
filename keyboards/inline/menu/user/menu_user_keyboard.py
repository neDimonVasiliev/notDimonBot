from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.db_api.db_commands_orders import select_order_by_telegram_id

async def gen_menu_user_keyboard(telegram_id: int):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Каталог",
                    switch_inline_query_current_chat=""
                )
            ],
        ]
    )
    orders = await select_order_by_telegram_id(telegram_id)
    print("Количество заказов", len(orders))
    if len(orders) > 0:
        orders_button = InlineKeyboardButton(text="Заказы", callback_data="orders_history")
        markup.row(orders_button)
    return markup
