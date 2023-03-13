from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.db_api.db_commands_orders import select_order_by_telegram_id
from aiogram.utils.callback_data import CallbackData

order_number_cd = CallbackData("order_number", "order_id")


async def gen_menu_orders_keyboard(telegram_id: int):
    markup = InlineKeyboardMarkup()
    orders = await select_order_by_telegram_id(telegram_id)
    print("Количество заказов", len(orders))
    for order in orders:
        order_button = InlineKeyboardButton(
            text=f"Заказ № {order.id}: {order.item_name} {order.item_quantity} {order.item_unit}",
            callback_data=order_number_cd.new(order_id=order.id))
        markup.row(order_button)
    return markup
