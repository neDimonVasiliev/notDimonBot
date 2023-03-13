from utils.db_api.database import db
from sqlalchemy import sql, Column, Sequence, Integer, DECIMAL


class User(db.Model):
    __tablename__ = "bot_user"

    query: sql.Select

    telegram_id = Column(db.Integer, Sequence("user_id_seq"), primary_key=True, autoincrement=False)
    username = Column(db.String(255))
    first_name = Column(db.String(255))
    last_name = Column(db.String(255))
    address = Column(db.Text)
    referral_telegram_id = Column(db.Integer)
    balance = Column(db.DECIMAL(10, 2))


class Item(db.Model):
    __tablename__ = "item"

    query: sql.Select

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    name = Column(db.String(255))
    description = Column(db.Text)
    photo = Column(db.String(255))
    price = Column(db.DECIMAL(10, 2))
    stock_quantity = Column(db.Integer)
    unit = Column(db.String(10))
    status = Column(db.String(20), default='available')


class Order(db.Model):
    __tablename__ = "customer_order"

    query: sql.Select

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    user_telegram_id = Column(db.Integer, db.ForeignKey('bot_user.telegram_id'))
    item_id = Column(db.Integer, db.ForeignKey('item.id'))
    item_quantity = Column(db.Integer)
    order_total_price = Column(db.DECIMAL(10, 2))
    order_currency = Column(db.String(10))
    delivery_address = Column(db.String(255))
    date = Column(db.Date)
    order_status = Column(db.String(20))
