from aiogram import types

from filters import IsPrivate
from keyboards.inline.menu.user.menu_user_keyboard import gen_menu_user_keyboard
from loader import dp
from aiogram.dispatcher.filters import Command
from data.config import admins

@dp.message_handler(IsPrivate(), Command("menu"))
async def user_menu(message: types.Message):
    markup = await gen_menu_user_keyboard(message.from_user.id)
    await message.answer(f"Вам доступны следующие функции:", reply_markup=markup)
