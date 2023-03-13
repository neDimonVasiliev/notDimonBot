from aiogram import types

from filters import IsPrivate
from loader import dp
from aiogram.dispatcher.filters import Command
from data.config import admins

from keyboards.inline.menu.admin.menu_admin_keyboard import menu_admin_keyboard

@dp.message_handler(IsPrivate(), Command("menu"), user_id=admins)
async def new_item(message: types.Message):
    markup = menu_admin_keyboard
    await message.answer(f"Вы являетесь администратором бота\n"
                         f"Вам доступны следующие функции:", reply_markup=markup)

