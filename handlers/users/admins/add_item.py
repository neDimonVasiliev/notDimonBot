from data.config import no_image_pic_url
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.menu.admin.cancel_add_item_keyboard import cancel_add_item_keyboard
from keyboards.inline.menu.admin.unit_add_item_keyboard import unit_add_item_keyboard
from keyboards.inline.menu.admin.confirm_add_item_keyboard import confirm_add_item_keyboard
from utils.db_api.db_commands_items import db_add_item
from typing import Union
from integrations.telegraph.abstract import FileUploader


@dp.callback_query_handler(state=["item_name",
                                  "item_description",
                                  "item_photo",
                                  "item_price",
                                  "item_quantity",
                                  "item_unit",
                                  "confirmation"],
                           text_contains="Cancel_add_item")
async def cancel_add_item(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.edit_text(text="Вы отменили добавление товара", reply_markup=None)
    await state.finish()


@dp.callback_query_handler(text_contains="Add_item")
async def add_item(call: types.CallbackQuery, state: FSMContext):
    callback_data = call
    print("callback_data: ", callback_data)
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state("item_name")
    await call.message.answer("Введите наименование товара", reply_markup=cancel_add_item_keyboard)


@dp.message_handler(state="item_name")
async def enter_item_name(message: types.Message, state: FSMContext):
    await state.update_data(itemName=message.text)
    await state.set_state("item_description")

    await message.answer("Введите описание товара", reply_markup=cancel_add_item_keyboard)


@dp.message_handler(state="item_description")
async def enter_item_description(message: types.Message, state: FSMContext):
    await state.update_data(itemDescription=message.text)
    await state.set_state("item_photo")

    await message.answer("Пришлите фото товара или введите символ \"-\", если у товара отсутствует фотография",
                         reply_markup=cancel_add_item_keyboard)


@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.TEXT, 'photo'], state="item_photo")
async def enter_item_photo(message, state: FSMContext, file_uploader: FileUploader):
    print(message.content_type)

    if message.content_type == "text":
        if message.text == "-":
            print(message)
            print(type(message))
            await state.update_data(itemPhoto=no_image_pic_url)
            await state.set_state("item_price")
            await message.answer("Введите цену товара, RUB", reply_markup=cancel_add_item_keyboard)

        else:
            print(message)
            print(type(message))
            await message.answer("Это не фотография. Если у товара нет фотографии, введите символ \"-\"",
                                 reply_markup=cancel_add_item_keyboard)
            await state.set_state("item_photo")
    else:
        print("Определили фото")
        photo_id = message.photo[-1].file_id

        photo = message.photo[-1]
        # await message.bot.send_chat_action(message.chat.id, 'upload_photo')
        uploaded_photo = await file_uploader.upload_photo(photo)
        # await message.answer(text=uploaded_photo.link)

        await message.answer("Введите цену товара, RUB.", reply_markup=cancel_add_item_keyboard)

        await state.update_data(itemPhoto=photo_id, itemPhotoUrl=uploaded_photo.link)
        await state.set_state("item_price")


@dp.message_handler(state="item_price")
async def enter_item_price(message: types.Message, state: FSMContext):
    try:
        await state.update_data(itemPrice=round(float(message.text), 2))
        await state.set_state("item_quantity")
        await message.answer("Укажите количество единиц товара на складе", reply_markup=cancel_add_item_keyboard)
    except ValueError:
        await state.set_state("item_price")
        await message.answer("Вы прислали некорректные данные.\n"
                             "Повторите ввод или нажмите кнопку \"Отмена\"", reply_markup=cancel_add_item_keyboard)

@dp.message_handler(state="item_quantity")
async def enter_item_price(message: types.Message, state: FSMContext):
    try:
        await state.update_data(itemQuantity=int(message.text))
        await state.set_state("item_unit")

        await message.answer("Выберите единицы измерения количества товара (на клавиатуре)",
                             reply_markup=unit_add_item_keyboard)
    except ValueError:
        await state.set_state("item_quantity")
        await message.answer("Вы прислали некорректные данные.\n"
                             "Повторите ввод или нажмите кнопку \"Отмена\"", reply_markup=cancel_add_item_keyboard)

@dp.callback_query_handler(state="item_unit")
async def cancel_add_item(call: types.CallbackQuery, state: FSMContext):
    units = {"unit_kilo": "кг.", "unit_gram": "г.", "unit_piece": "шт.", "unit_liter": "л.", "unit_package": "уп."}
    print(call.data)
    await state.update_data(itemUnit=units[call.data])
    data = await state.get_data()
    print("data:", data)
    await call.answer(cache_time=60)
    if data["itemPhoto"] == "no picture":
        await call.message.edit_text(text=f"Вы закончили ввод информации о товаре\n"
                                          f"Фото: отсутствует\n"
                                          f"Наименование: {data['itemName']}\n"
                                          f"Описание: {data['itemDescription']}\n"
                                          f"Стоимость {data['itemPrice']} RUB\n"
                                          f"Количество на складе: {data['itemQuantity']} {data['itemUnit']}\n"
                                          f"\n"
                                          f"Подтвердить?",
                                     reply_markup=confirm_add_item_keyboard
                                     )

    else:
        await bot.send_message(chat_id=call["message"]["chat"]["id"], text="Вы закончили ввод информации о товаре")
        await bot.send_photo(chat_id=call["message"]["chat"]["id"],
                             photo=data["itemPhoto"],
                             caption=f"Наименование: {data['itemName']}\n"
                                     f"Описание: {data['itemDescription']}\n"
                                     f"Стоимость: {data['itemPrice']} RUB\n"
                                     f"Количество на складе: {data['itemQuantity']} {data['itemUnit']}\n"
                                     f"\n"
                                     f"Подтвердить?",
                             reply_markup=confirm_add_item_keyboard)

        await call.message.edit_reply_markup(reply_markup=None)

    await state.set_state("confirmation")


@dp.callback_query_handler(state="confirmation", text_contains="Confirm_item")
async def confirm_add_item(call: types.CallbackQuery, state: FSMContext):
    print("Callback Подтвердить")
    data = await state.get_data()
    print(data["itemName"])
    await db_add_item(name=data["itemName"],
                      description=data["itemDescription"],
                      photo=data["itemPhoto"], # было photo=data["itemPhotoUrl"]
                      price=data["itemPrice"],
                      stock_quantity=data["itemQuantity"],
                      unit=data["itemUnit"])

    await call.answer(cache_time=60)
    await bot.send_message(chat_id=call["message"]["chat"]["id"], text="Товар добавлен в базу данных")
    await call.message.edit_reply_markup(reply_markup=None)
    await state.finish()
