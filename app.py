from asyncpg import UniqueViolationError

from integrations.telegraph.service import TelegraphService
from middlewares.integration import IntegrationMiddleware
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.database import create_db
import filters
import middlewares

from utils.db_api.add_to_database_users import add_main_referral

async def on_startup(dp):
    filters.setup(dp)
    middlewares.setup(dp)

    await on_startup_notify(dp)
    await set_default_commands(dp)

    await create_db()
    try:
        await add_main_referral()
    except UniqueViolationError:
        pass

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    file_uploader = TelegraphService()

    dp.middleware.setup(IntegrationMiddleware(file_uploader))
    executor.start_polling(dp, on_startup=on_startup)
