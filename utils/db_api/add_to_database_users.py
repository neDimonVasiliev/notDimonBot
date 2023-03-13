from utils.db_api.db_commands_users import add_user, add_balance, check_balance
import asyncio
from utils.db_api.database import create_db


async def add_main_referral():
    await add_user(
        telegram_id=999999999,
        username="GodUser",
        balance=0
    )
    # await add_balance(telegram_id=999999999, value=10)
    # await check_balance(1851337609)
# Раскомментировать для локальных тестов команд
# loop = asyncio.get_event_loop()
# loop.run_until_complete(create_db())
# loop.run_until_complete(add_main_referral())
