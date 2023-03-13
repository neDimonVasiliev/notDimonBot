from aiogram import types
from aiogram.dispatcher.filters import Command, CommandStart

from keyboards.inline.menu.items.start_item_keyboard import start_item_keyboard_data
# from data.config import allowed_users
from loader import dp, bot
from utils.db_api.db_commands_items import select_all_items, find_items
from utils.db_api.db_commands_users import check_user
from aiogram.types import ReplyKeyboardRemove, CallbackQuery

from keyboards.inline.menu.admin.cancel_add_item_keyboard import cancel_add_item_keyboard

allowed_users = []  # [1851337609]


# функция формирования результатов поиска
async def gen_result(query, telegram_id):
    items = await find_items(query, telegram_id)
    results = []
    for item in items:
        results.append(
            types.InlineQueryResultArticle(
                id=item.id,
                title=item.name,
                input_message_content=types.InputTextMessageContent(
                    message_text=f"{item.photo}\n"
                                 f"{item.name}\n"
                                 f"{item.description}",
                    parse_mode="HTML",
                ),
                # url="https://core.telegram.org/bots/api#inlinequeryresult",
                thumb_url=item.photo,
                description=item.description,
                reply_markup=await start_item_keyboard_data(item_id=item.id)
            ),
        )
    print(results)
    return results


@dp.inline_handler(text="")
async def empty_query(query: types.InlineQuery):
    user = await check_user(query.from_user.id)
    print("user: ", user)
    if user is not None:
        await query.answer(
            results=await gen_result("", telegram_id=query.from_user.id),
            cache_time=5)
    else:
        await query.answer(
            results=[],
            switch_pm_text="Вы не зарегистрированы. Зарегистрироваться.",
            switch_pm_parameter="register_from_inline_menu",
            cache_time=5)
        return


@dp.inline_handler()
async def empty_query(query: types.InlineQuery):
    user = await check_user(query.from_user.id)
    print("user: ", user)
    if user is not None:
        if len(query.query) >= 2:
            print(len(query.query))
            await query.answer(
                results=await gen_result(query.query, telegram_id=query.from_user.id)
            )
    else:
        await query.answer(
            results=[],
            switch_pm_text="Вы не зарегистрированы. Зарегистрироваться.",
            switch_pm_parameter="register_from_inline_menu",
            cache_time=5)
        return



