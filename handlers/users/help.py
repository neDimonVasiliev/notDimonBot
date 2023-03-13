from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! \n"
                         f"Чтобы посмотреть список доступных команд, жми /menu\n")
