from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.menu.user.menu_orders_keyboard import gen_menu_orders_keyboard, order_number_cd
from loader import dp
from utils.db_api.db_commands_orders import select_order_by_telegram_id, select_order_by_order_id


@dp.callback_query_handler(text_contains="orders_history")
async def call_primer(call: types.CallbackQuery, state: FSMContext):
    orders = await select_order_by_telegram_id(call.from_user.id)
    for order in orders:
        print(order.id)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Выберите ваш заказ:\n",
                              reply_markup=await gen_menu_orders_keyboard(call.from_user.id))


@dp.callback_query_handler(order_number_cd.filter())
async def call_buy_item(call: CallbackQuery, callback_data: dict, state: FSMContext):
    print(callback_data)
    await call.message.edit_reply_markup(reply_markup=None)
    order = await select_order_by_order_id(order_id=int(callback_data["order_id"]), telegram_id=call.from_user.id)
    print("order: ", order)
    # await call.message.answer(f"Тестируем хенделер заказа")
    await call.message.answer(f"Номер заказа: {order.id}\n"
                              f"Дата заказа: {order.date}\n"
                              f"Товар: {order.item_name}\n"
                              f"Количество: {order.item_quantity} {order.item_unit}\n"
                              f"Общая стоимость: {order.order_total_price} {order.order_currency}\n"
                              f"Адрес доставки: {order.delivery_address}\n",
                              reply_markup=None)
