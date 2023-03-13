from utils.db_api.db_commands_items import db_add_item, find_items
import asyncio
from utils.db_api.database import create_db


async def add_test_item():
    await db_add_item(
        name="test",
    )

async def search():
    await find_items("ани", telegram_id=1851337609)

# Раскомментировать для локальных тестов команд
loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
# loop.run_until_complete(add_test_item())
loop.run_until_complete(search())
