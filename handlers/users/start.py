from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove, CallbackQuery

from keyboards.inline.new_user.confirm_register_keyboard import confirm_register_keyboard_data, confirm_register_cd
from utils.db_api.db_commands_users import referral_ids

from aiogram.dispatcher import FSMContext

from filters import IsPrivate
from loader import dp
from re import compile
from utils.db_api.db_commands_users import check_user, add_user, add_balance
from keyboards.inline.new_user.register_keyboard import register_keyboard


# пользователь пришел из inline menu, где у него не было возможности ввести referral id
@dp.message_handler(CommandStart(deep_link="register_from_inline_menu"), IsPrivate())
async def bot_start(message: types.Message):
    bot_user = await dp.bot.get_me()

    user = await check_user(message.from_user.id)
    if user is None:
        await message.answer(f"Привет, {message.from_user.full_name}!\n"
                             f"Для регистрации необходимо ввести id реферала. \n"
                             f"Если вы пришли по объявлению, жмите кнопку \"По объявлению\".\n"
                             f"Если вы хотите ввести id реферала вручную, жмите кнопку \"Ввести id вручную\".\n"
                             f"Если вы хотите отменить регистрацию, жмите кнопку \"Отмена\".",
                             reply_markup=register_keyboard)
    else:
        await message.answer("Вы уже были зарегистрированы ранее. Чтобы посмотреть список доступных команд, жми /help")


# referral_id указан в правильном формате, но пользователь с таким referral_id не зарегистрирован
@dp.message_handler(CommandStart(deep_link=compile(r"\d{3,10}")), IsPrivate())
async def bot_start_deeplink(message: types.Message):
    deep_link_arg = int(message.get_args())

    user = await check_user(message.from_user.id)

    if user is None:

        referral_user = await check_user(deep_link_arg)
        if referral_user is None:
            await message.answer(f"Пользователь с telegram_id {deep_link_arg} не зарегистрирован.\n"
                                 f"Если вы пришли по объявлению, жмите кнопку \"По объявлению\".\n"
                                 f"Если вы хотите ввести id реферала вручную, жмите кнопку \"Ввести id вручную\".\n"
                                 f"Если вы хотите отменить регистрацию, жмите кнопку \"Отмена\".",
                                 reply_markup=register_keyboard)
        else:
            markup = await confirm_register_keyboard_data(deep_link_arg)
            await message.answer(f"Поздравляем! \n"
                                 f"Ваши учетные данные:\n"
                                 f"telegram_id: {message.from_user.id}\n"
                                 f"username: {message.from_user.username}\n"
                                 f"first_name: {message.from_user.first_name}\n"
                                 f"last_name: {message.from_user.last_name}\n"
                                 f"referral_telegram_id: {deep_link_arg}\n"
                                 f"Баланс: 0 Бонусов"
                                 f"\n"
                                 f"Подтвердить регистрацию?", reply_markup=markup)

    else:
        await message.answer("Вы уже были зарегистрированы ранее. Чтобы посмотреть список доступных команд, жми /help")


# referral_id не указан
@dp.message_handler(CommandStart(deep_link=None), IsPrivate())
async def bot_start(message: types.Message):
    bot_user = await dp.bot.get_me()

    user = await check_user(message.from_user.id)
    if user is None:
        await message.answer(f"Привет, {message.from_user.full_name}!\n"
                             f"Вы указали некорректный referral_id. \n"
                             f"Если вы пришли по объявлению, жмите кнопку \"По объявлению\".\n"
                             f"Если вы хотите ввести id реферала вручную, жмите кнопку \"Ввести id вручную\".\n"
                             f"Если вы хотите отменить регистрацию, жмите кнопку \"Отмена\".",
                             reply_markup=register_keyboard)
    else:
        await message.answer("Вы уже были зарегистрированы ранее. Чтобы посмотреть список доступных команд, жми /help")


# ввод referral_id вручную
@dp.callback_query_handler(text_contains="Enter_id_manually")
async def call_primer(call: types.CallbackQuery, state: FSMContext):
    callback_data = call.data
    print("callback_data: ", callback_data)
    await state.set_state("enter_referral_id")
    await call.answer(cache_time=60)
    await call.message.edit_text("Введите id реферала вручную")


# переход к вводу referral_id вручную
@dp.message_handler(state="enter_referral_id")
async def enter_referral_id(message: types.Message, state: FSMContext):
    check_id = await referral_ids(message.text)
    print("check_id: ", check_id)

    if check_id:
        await state.finish()
        markup = await confirm_register_keyboard_data(message.text)
        await message.answer(f"Поздравляем! \n"
                             f"Ваши учетные данные:\n"
                             f"telegram_id: {message.from_user.id}\n"
                             f"username: {message.from_user.username}\n"
                             f"first_name: {message.from_user.first_name}\n"
                             f"last_name: {message.from_user.last_name}\n"
                             f"referral_telegram_id: {message.text}\n"
                             f"Баланс: 0 Бонусов"
                             f"\n"
                             f"Подтвердить регистрацию?", reply_markup=markup)

    else:
        await state.finish()
        await message.answer(f"Вы некорректно указали referral_id. Должны быть указаны только цифры."
                             f"Если вы пришли по объявлению, жмите кнопку \"По объявлению\".\n"
                             f"Если вы хотите ввести id реферала вручную, жмите кнопку \"Ввести id вручную\"."
                             f"Если вы хотите отменить регистрацию, жмите кнопку \"Отмена\".",
                             reply_markup=register_keyboard)


# По объявлению
@dp.callback_query_handler(text_contains="Advertisement")
async def call_advertisement(call: types.CallbackQuery):
    callback_data = call.data
    print("callback_data: ", callback_data)
    await call.answer(cache_time=60)
    markup = await confirm_register_keyboard_data(999999999)
    await call.message.edit_text(f"Поздравляем! \n"
                                 f"Ваши учетные данные:\n"
                                 f"telegram_id: {call.from_user.id}\n"
                                 f"username: {call.from_user.username}\n"
                                 f"first_name: {call.from_user.first_name}\n"
                                 f"last_name: {call.from_user.last_name}\n"
                                 f"referral_telegram_id: {999999999}\n"
                                 f"Баланс: 0 Бонусов"
                                 f"\n"
                                 f"Подтвердить регистрацию?", reply_markup=markup)


# Подтверждение регистрации
@dp.callback_query_handler(confirm_register_cd.filter())
async def call_confirm_registration(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    print(callback_data)
    referral_telegram_id = int(callback_data.get("referral_id"))
    user = await add_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        address=None,
        referral_telegram_id=referral_telegram_id,
        balance=0
    )
    await add_balance(telegram_id=referral_telegram_id, value=1000)
    await call.message.edit_text(f"Поздравляем! Регистрация завершена.", reply_markup=None)


# Отмена регистрации
@dp.callback_query_handler(text_contains="Cancel_registration")
async def call_cancel_registration(call: types.CallbackQuery):
    callback_data = call
    print("callback_data: ", callback_data)
    await call.answer(cache_time=60)
    await call.message.edit_text("Вы отменили регистрацию. Чтобы продолжить работу с ботом, необходимо "
                                 "зарегистрироваться.")
