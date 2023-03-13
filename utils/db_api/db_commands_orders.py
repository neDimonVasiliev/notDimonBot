from utils.db_api.database import db
from utils.db_api.models import Order
from data.config import admins


async def db_add_order(**kwargs):
    new_order = await Order(**kwargs).create()
    return new_order


async def select_all_orders():
    orders = await Order.query.gino.all()
    for order in orders:
        print(order.id)
    return orders


# async def select_order_by_order_id(order_id: int):
#     order = await Order.query.where(Order.id == order_id).gino.first()
#     return order

async def select_order_by_order_id(order_id: int, telegram_id: int):
    SQL = " \
    SELECT customer_order.id AS id, \
    customer_order.user_telegram_id  AS user_telegram_id , \
    customer_order.item_id AS item_id, \
    customer_order.item_quantity AS item_quantity, \
    customer_order.order_total_price AS order_total_price, \
    customer_order.order_currency AS order_currency, \
    customer_order.delivery_address AS delivery_address, \
    customer_order.date AS date, \
    customer_order.order_status AS order_status, \
    item.name AS item_name, \
    item.description AS item_description,\
    item.photo AS item_photo, \
    item.unit AS item_unit \
    FROM customer_order INNER JOIN item ON customer_order.item_id = item.id \
    WHERE customer_order.id = :order_id AND customer_order.user_telegram_id = :telegram_id \
    "
    query = db.text(SQL)
    order = await db.first(query, order_id=order_id, telegram_id=telegram_id)
    print("order внутри функции: ", order, order.item_name, order.id)
    return order


async def select_order_by_telegram_id(telegram_id: int):
    SQL = " \
    SELECT customer_order.id AS id, \
    customer_order.user_telegram_id  AS user_telegram_id , \
    customer_order.item_id AS item_id, \
    customer_order.item_quantity AS item_quantity, \
    customer_order.order_total_price AS order_total_price, \
    customer_order.order_currency AS order_currency, \
    customer_order.delivery_address AS delivery_address, \
    customer_order.date AS date, \
    customer_order.order_status AS order_status, \
    item.name AS item_name, \
    item.description AS item_description,\
    item.photo AS item_photo, \
    item.unit AS item_unit \
    FROM customer_order INNER JOIN item ON customer_order.item_id = item.id \
    WHERE customer_order.user_telegram_id = :telegram_id \
    "
    query = db.text(SQL)
    orders = await db.all(query, telegram_id=telegram_id)
    for order in orders:
        print(order.id, order.item_name)
    return orders


async def update_order_status(order_id: int, status):
    order = await Order.get(order_id)
    order = await order.update(order_status="payment_done").apply()
    return order
