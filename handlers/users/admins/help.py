from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp

from data.config import admins
from filters import IsPrivate
from loader import dp


@dp.message_handler(CommandHelp(), IsPrivate(), user_id=admins)
async def bot_help(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! \n"
                         f"Вы являетесь администратором, поэтому вам досупно больше команд.\n"
                         f"Чтобы посмотреть список доступных команд, жми /menu\n")
