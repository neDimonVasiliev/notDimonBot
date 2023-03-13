from aiogram import types
from loader import dp


@dp.message_handler(text="Димон")
async def dimon(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    await message.reply(text="Он вам не Димон!")


@dp.message_handler()
async def echo(message: types.Message):
    # Получим chat_id и text
    chat_id = message.from_user.id
    text = message.text

    # Получим объект бота - вариант 1 (из диспатчера)
    # bot = dp.bot

    # Получим объект бота - вариант 2 (из контекста)
    # from aiogram import Bot
    # bot = Bot.get_current()

    # Получим объект бота - вариант 3 (из модуля loader)
    from loader import bot
    await bot.send_message(chat_id=chat_id, text=text)
    # await message.answer(text=text)
    # await message.reply(text=text)


