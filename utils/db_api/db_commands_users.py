from utils.db_api.database import db
from utils.db_api.models import User
from typing import List


async def add_user(**kwargs):
    new_user = await User(**kwargs).create()
    return new_user


async def check_user(telegram_id):
    SQL = """
    SELECT * FROM bot_user WHERE telegram_id = :telegram_id
    """
    query = db.text(SQL)
    user = await db.scalar(query, telegram_id=telegram_id)
    print(user)
    return user


async def referral_ids(ref_id: str):
    try:
        if isinstance(int(ref_id), int):
            ref_id = int(ref_id)
    except ValueError:
        return False

    SQL = """
    SELECT telegram_id AS id FROM bot_user
    """
    query = db.text(SQL)
    ids = await db.all(query)

    for i in range(0, len(ids)):
        print(int(ids[i][0]))
        print(ref_id)
        if ref_id == int(ids[i][0]):
            print("True")
            return True
        else:
            print("False")
            return False


async def add_balance(telegram_id, value):
    user = await User.get(telegram_id)
    user = await user.update(balance=User.balance + value).apply()
    return user


async def check_balance(telegram_id: int) -> float:
    user = await User.query.where(User.telegram_id == telegram_id).gino.first()
    print("user.balance: ", user.balance)
    return user.balance


# async def update_user_email(id, email):
#     user = await User.get(id)
#     await user.update(email=email).apply()

# UPDATE bot_user SET balance=(bot_user.balance + $1) WHERE bot_user.telegram_id = $2
