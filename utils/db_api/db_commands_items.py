from utils.db_api.database import db
from utils.db_api.models import Item
from data.config import admins


async def select_all_items():
    items = await Item.query.gino.all()
    for item in items:
        print(item.id)
    return items


async def db_add_item(**kwargs):
    new_item = await Item(**kwargs).create()
    return new_item


async def find_items(request: str, telegram_id):
    if telegram_id in admins:
        SQL = """
        SELECT * FROM item WHERE name ILIKE :request or description ILIKE :request;
        """
    else:  # если пользователь не админ, то ему недоступны товары со статусом unavailable
        SQL = """
        SELECT * FROM item WHERE (name ILIKE :request or description ILIKE :request) and status='available';
        """
    query = db.text(SQL)
    items = await db.all(query, request="%" + request + "%")
    print("admins: ", admins)
    print("SQL: ", SQL)
    print("Результаты поиска")
    print(items)
    for item in items:
        print(item.name)
    return items


async def select_item(item_id: int):
    item = await Item.query.where(Item.id == item_id).gino.first()
    return item


async def reduce_item_amount(item_id: int, amount: int):
    item = await Item.get(item_id)
    item = await item.update(stock_quantity=Item.stock_quantity - amount).apply()
    return item

async def update_item(item_id, param, value):
    item = await Item.get(item_id)
    if param == "name":
        await item.update(name=value).apply()
    if param == "description":
        await item.update(description=value).apply()
    if param == "photo":
        await item.update(photo=value).apply()
    if param == "price":
        await item.update(price=value).apply()
    if param == "stock_quantity":
        await item.update(stock_quantity=value).apply()
    if param == "unit":
        await item.update(unit=value).apply()
    if param == "status":
        await item.update(status=value).apply()
