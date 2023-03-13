from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.menu.items.confirm_buy_balance_keyboard import confirm_buy_item_balance_keyboard
from keyboards.inline.menu.items.confirm_buy_paymaster_keyboard import confirm_buy_item_paymaster_keyboard
from keyboards.inline.menu.items.confirm_delivery_address_keyboard import confirm_delivery_address_keyboard
from loader import dp, bot
from re import compile
from utils.db_api.db_commands_items import select_item, reduce_item_amount
from utils.db_api.db_commands_users import check_balance, add_balance
from utils.db_api.db_commands_orders import db_add_order, update_order_status
from keyboards.inline.menu.items.show_item_keyboard import show_item_keyboard_data, buy_item_cd
from keyboards.inline.menu.items.cancel_buy_item_keyboard import cancel_buy_item_keyboard
from keyboards.inline.menu.items.payment_method_keyboard import payment_method_keyboard
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType

from data.config import PAYMASTER_TOKEN
from data.config import admins


@dp.callback_query_handler(state=["show_item",
                                  "enter_item_amount",
                                  "delivery_address",
                                  "confirm_delivery_address",
                                  "payment_method",
                                  "confirm_buy_item_bonus",
                                  "confirm_buy_item_paymaster"],
                           text_contains="Cancel_buy_item")
async def cancel_add_item(call: types.CallbackQuery, state: FSMContext):
    print("callback отмены покупки товара ", "state: ", await state.get_state())
    current_state = await state.get_state()
    print("current_state: ", current_state)
    if current_state != "show_item":
        await call.message.edit_reply_markup(reply_markup=None)
        await call.answer(cache_time=60)
        await call.message.edit_text(text="Вы отменили покупку товара", reply_markup=None)
    else:
        await call.message.edit_reply_markup(reply_markup=None)
        await call.answer(cache_time=60)

    await state.finish()
    print("state: ", await state.get_state())


@dp.message_handler(CommandStart(deep_link=compile(r"^item_id-\d{1,10}")))
async def show_item(message: types.Message, state: FSMContext):
    deep_link_args = message.get_args()
    item_id = int(deep_link_args[8:])
    print("deep_link_args: ", deep_link_args)
    print("item_id: ", item_id)
    item = await select_item(item_id)
    if message.from_user.id in admins:
        text = f"Наименование: {item.name}\n" \
               f"Описание: {item.description}\n" \
               f"Стоимость: {item.price} RUB\n" \
               f"Количество на складе: {item.stock_quantity} {item.unit}\n" \
               f"Статус товара: {item.status}"
    else:
        text = f"Наименование: {item.name}\n" \
               f"Описание: {item.description}\n" \
               f"Стоимость: {item.price} RUB\n" \
               f"Количество на складе: {item.stock_quantity} {item.unit}\n" \

    await state.set_state("show_item")
    await message.answer("Обработка хендлера, чтобы показать товар")
    await bot.send_photo(chat_id=message.chat.id,
                         photo=item.photo,
                         caption=text,
                         reply_markup=await show_item_keyboard_data(item_id, telegram_id=message.from_user.id))


@dp.callback_query_handler(buy_item_cd.filter(), state="show_item")
async def call_buy_item(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    print(callback_data)
    await call.message.edit_reply_markup(reply_markup=None)

    await call.message.answer("Введите количество товара или нажмите кнопку \"Отменить\"",
                              reply_markup=cancel_buy_item_keyboard)

    await state.update_data(item_id=int(callback_data.get("item_id")))
    await state.set_state("enter_item_amount")


@dp.message_handler(state="enter_item_amount")
async def enter_item_amount(message: types.Message, state: FSMContext):
    try:
        await state.update_data(item_quantity=int(message.text))
        await state.set_state("delivery_address")
        data = await state.get_data()
        print("data: ", data)
        item = await select_item(int(data["item_id"]))
        total_order_price = data["item_quantity"] * item.price
        await state.update_data(total_order_price=total_order_price)
        await message.answer(f"Стоимость вашего заказа: {total_order_price} RUB.\n"
                             "Введите адрес доставки товара или нажмите кнопку \"Отменить\".",
                             reply_markup=cancel_buy_item_keyboard)

    except ValueError:
        await message.answer("Введите целое число или нажмите кнопку \"Отменить\"",
                             reply_markup=cancel_buy_item_keyboard)
        await state.set_state("enter_item_amount")


# ввод адреса доставки
@dp.message_handler(state="delivery_address")
async def enter_item_address(message: types.Message, state: FSMContext):
    await state.update_data(delivery_address=message.text)
    await state.set_state("confirm_delivery_address")
    await state.update_data(delivery_address=message.text)
    await message.answer(f"Адрес доставки товара: {message.text}\n"
                         f"Адрес доставки указан верно?",
                         reply_markup=confirm_delivery_address_keyboard)


# исправление адреса доставки
@dp.callback_query_handler(state="confirm_delivery_address",
                           text_contains="Edit_delivery_address")
async def confirm_delivery_address(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state("delivery_address")
    await call.message.edit_text("Введите адрес доставки товара или нажмите кнопку \"Отменить\"",
                                 reply_markup=cancel_buy_item_keyboard)


# подтверждение адреса доставки
@dp.callback_query_handler(state="confirm_delivery_address",
                           text_contains="Confirm_delivery_address")
async def confirm_delivery_address(call: types.CallbackQuery, state: FSMContext):
    print("callback подтверждения адреса доставки ", "state: ", await state.get_state())
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(cache_time=60)
    await state.set_state("payment_method")

    await call.message.edit_text(text="Адрес доставки подтвержден.\n"
                                      "Выберите способ оплаты товара или нажмите кнопку \"Отменить\".",
                                 reply_markup=payment_method_keyboard)
    print("state: ", await state.get_state())


# покупка за бонусы
@dp.callback_query_handler(state="payment_method",
                           text_contains="Bonus_payment_method")
async def payment_bonus(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print("data: ", data)
    balance = await check_balance(call.from_user.id)
    print("call.from_user.id: ", call.from_user.id)
    print(type(call.from_user.id))
    print("Баланс: ", balance)
    item = await select_item(int(data["item_id"]))
    if balance < data["total_order_price"]:
        await call.message.edit_reply_markup(reply_markup=None)
        await state.set_state("payment_method")
        await call.message.answer(f"Ошибка!\n"
                                  f"Баланс {balance} Бонусов меньше общей стоимости товара {data['total_order_price']} Бонусов.\n"
                                  f"Выберите другой способ оплаты или нажмите кнопку \"Отменить\".",
                                  reply_markup=payment_method_keyboard)
    else:
        await call.message.edit_reply_markup(reply_markup=None)
        await state.set_state("confirm_buy_item_bonus")
        await call.message.answer(f"Параметры Вашего заказа:\n"
                                  f"{item.name} {data['item_quantity']} {item.unit}\n"
                                  f"Общая стоимость: {data['total_order_price']} Бонусов\n"
                                  f"Ваш баланс: {balance} Бонусов\n"
                                  f"Подтвердите заказ или нажмите кнопку \"Отменить\".\n"
                                  f"",
                                  reply_markup=confirm_buy_item_balance_keyboard)


# Подтверждение покупки за бонусы и запись заказа в БД
@dp.callback_query_handler(state="confirm_buy_item_bonus",
                           text_contains="Confirm_buy_item_balance")
async def confirm_payment_bonus(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await add_balance(telegram_id=call.from_user.id, value=-data['total_order_price'])

    order = await db_add_order(user_telegram_id=call.from_user.id,
                               item_id=int(data["item_id"]),
                               item_quantity=int(data["item_quantity"]),
                               order_total_price=data['total_order_price'],
                               order_currency="BONUS",
                               delivery_address=data['delivery_address'],
                               date=None,
                               order_status="payment_done")

    await reduce_item_amount(item_id=int(data["item_id"]), amount=int(data["item_quantity"]))
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(f"Поздравляем!\n"
                              f"Ваш заказ успешно оформлен!\n"
                              f"Ваш баланс после заказа составляет: {await check_balance(call.from_user.id)} Бонусов\n"
                              f"С Вами свяжется оператор для уточнения деталей доставки.",
                              reply_markup=None)
    await state.finish()


# QIWI способ оплаты
@dp.callback_query_handler(state="payment_method",
                           text_contains="PAYMASTER_payment_method")
async def payment_paymaster(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print("data: ", data)
    item = await select_item(int(data["item_id"]))
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state("confirm_buy_item_paymaster")
    await call.message.answer(f"Вы выбрали способ оплаты PAYMASTER:\n"
                              f"Параметры Вашего заказа:\n"
                              f"{item.name} {data['item_quantity']} {item.unit}\n"
                              f"Общая стоимость: {data['total_order_price']} RUB\n"
                              f"Подтвердите заказ или нажмите кнопку \"Отменить\".\n",
                              reply_markup=confirm_buy_item_paymaster_keyboard)


@dp.callback_query_handler(state="confirm_buy_item_paymaster",
                           text_contains="Confirm_buy_item_paymaster")
async def payment_paymaster(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print("data: ", data)
    item = await select_item(int(data["item_id"]))
    price = types.LabeledPrice(label=f"{item.name} {data['item_quantity']} {item.unit}",
                               amount=(int(data['total_order_price']) * 100))
    await state.set_state("send_invoice")
    await bot.send_invoice(call.from_user.id,
                           title="Заказик",
                           description="Тестовый дескрипшн",
                           provider_token=PAYMASTER_TOKEN,
                           currency="rub",
                           prices=[price],
                           start_parameter="zakupochka",
                           payload="покупочка")


@dp.pre_checkout_query_handler(state="send_invoice")
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery, state: FSMContext):
    print("ловим хендлер pre_checkout_query")
    data = await state.get_data()

    order = await db_add_order(user_telegram_id=pre_checkout_q.from_user.id,
                               item_id=int(data["item_id"]),
                               item_quantity=int(data["item_quantity"]),
                               order_total_price=data['total_order_price'],
                               order_currency="RUB",
                               delivery_address=data['delivery_address'],
                               date=None,
                               order_status="payment_pending")
    await state.update_data(order_id=order.id)
    await state.set_state("successful_payment")
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT, state="successful_payment")
async def successful_payment(message: types.Message, state: FSMContext):
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k}, {v}")
    data = await state.get_data()
    order = await update_order_status(order_id=int(data["order_id"]), status="payment_done")
    await reduce_item_amount(item_id=int(data["item_id"]), amount=int(data["item_quantity"]))
    await state.finish()
    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} RUB обработан успешно.\n"
                           f"С Вами свяжется оператор для уточнения деталей доставки.")

