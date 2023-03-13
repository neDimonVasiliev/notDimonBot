from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.types import CallbackQuery

from data.config import admins, no_image_pic_url
from keyboards.inline.menu.admin.confirm_edit_item_param_keyboard import confirm_edit_item_parameter_keyboard
from keyboards.inline.menu.admin.continue_edit_item_keyboard import continue_edit_item_keyboard
from keyboards.inline.menu.admin.edit_item_keyboard import edit_item_keyboard_data, edit_item_name_cd
from keyboards.inline.menu.admin.edit_item_repeat_input_or_cancel_keyboard import \
    edit_item_repeat_input_or_cancel_keyboard
from keyboards.inline.menu.admin.edit_item_status_keyboard import edit_item_status_keyboard
from keyboards.inline.menu.admin.unit_add_item_keyboard import unit_add_item_keyboard
from loader import dp, bot

from keyboards.inline.menu.items.show_item_keyboard import edit_item_cd
from utils.db_api.db_commands_items import update_item, select_item
from integrations.telegraph.abstract import FileUploader


@dp.callback_query_handler(edit_item_cd.filter(), state="show_item")
async def call_edit_item(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    print(callback_data)
    await call.message.edit_reply_markup(reply_markup=None)
    markup = await edit_item_keyboard_data(item_id=int(callback_data["item_id"]))
    await state.finish()
    await call.message.answer("Выберите параметр товара, который необходимо изменить",
                              reply_markup=markup)


@dp.callback_query_handler(text_startswith="finish_edit_item")
async def finish_edit_item(call: CallbackQuery, state: FSMContext):
    print("Словили хендлер закончить редактирование товара")
    print("call.message: ", call.message)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Вы отменили/завершили редактирование товара", reply_markup=None)
    await state.finish()


# обработка отмены при подтверждении параметра товара (меню с 2 кнопками)
@dp.callback_query_handler(text_startswith="Cancel_edit_item_parameter", state=["confirm_edit_item_parameter", None])
async def finish_edit_item_from_confirmation(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Вы отменили/завершили редактирование товара", reply_markup=None)
    await state.finish()


# хендлер, в котором ловим callback от нажатия кнопки с выбором параметра товара, который редактируем
@dp.callback_query_handler(text_startswith="edit_item_")
async def call_edit_item_parameter(call: CallbackQuery, state: FSMContext):
    cb_data = {call.data.split(":")[0]: int(call.data.split(":")[1])}
    action = call.data.split(":")[0]
    item_id = int(call.data.split(":")[1])
    item = await select_item(item_id)
    await state.update_data(action=action, item_id=item_id)

    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)

    if action == "edit_item_name":
        await call.message.answer("Введите новое имя товара")
    if action == "edit_item_description":
        await call.message.answer("Введите новое описание товара")
    if action == "edit_item_photo":
        await call.message.answer("Пришлите новое фото товара или введите символ \"-\", если хотите удалить фото")
    if action == "edit_item_price":
        await call.message.answer("Введите новую цену товара, RUB.")
    if action == "edit_item_stock_quantity":
        await call.message.answer("Введите новое количество товара на складе")
    if action == "edit_item_unit":
        await state.set_state("edit_item_unit")
        await call.message.answer("Выберите новые единицы измерения количества товара\n",
                                  reply_markup=unit_add_item_keyboard)

    if action == "edit_item_status":
        await state.set_state("edit_item_status")
        await call.message.answer("Чтобы изменить статус товара, нажмите кнопку с новым статусом.",
                                  reply_markup=await edit_item_status_keyboard(item.status))

    if action not in ["edit_item_unit", "edit_item_status"]:  # ввод данных осуществляется с помощью callback, поэтому обрабатываем в отдельном хенделере
        await state.set_state("edit_item_parameter")


# отдельный хендлер для редактирования единиц измерения товара и его статуса
@dp.callback_query_handler(state=["edit_item_unit", "edit_item_status"])
async def call_edit_item_unit_parameter(call: CallbackQuery, state: FSMContext):
    units = {"unit_kilo": "кг.", "unit_gram": "г.", "unit_piece": "шт.", "unit_liter": "л.", "unit_package": "уп."}
    await call.message.edit_reply_markup(reply_markup=None)
    print("call.data: ", call.data)
    if call.data in ["Cancel_add_item", "Cancel_edit_item_parameter"]:  # потому что используем клавиатуру для добавления товара
        if call.data == "Cancel_add_item":
            text = "единиц измерения"
        else:
            text = "статуса"
        await call.message.edit_text(f"Вы отменили редактирование {text} товара.", reply_markup=None)
        await state.finish()

    if call.data in units.keys():
        data = await state.get_data()
        markup = await confirm_edit_item_parameter_keyboard(item_id=data["item_id"], parameter="edit_item_unit")
        await state.update_data(item_unit=units[call.data])
        await call.message.answer(f"Новые единицы измерения товара: {units[call.data]}\n"
                                  f"Подтвердить?",
                                  reply_markup=markup)
        await state.set_state("confirm_edit_item_parameter")
    if call.data in ["available", "unavailable"]:
        data = await state.get_data()
        markup = await confirm_edit_item_parameter_keyboard(item_id=data["item_id"], parameter="edit_item_status")
        await state.update_data(item_status=call.data)
        await call.message.answer(f"Новый статус товара: {call.data}\n"
                                  f"Подтвердить?",
                                  reply_markup=markup)
        await state.set_state("confirm_edit_item_parameter")

# хендлер, в котором обрабатываем ввод данных для изменяемого параметра товара
@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.TEXT, 'photo'],
                    state="edit_item_parameter")
async def edit_item_parameter(message: types.Message, state: FSMContext, file_uploader: FileUploader):
    await state.set_state(
        "confirm_edit_item_parameter")  # если не было ошибки валидации, то state = confirm_edit_item_parameter
    data = await state.get_data()
    print("data: ", data)
    print("item_id: ", data["item_id"])
    action = data["action"]
    print("action: ", action)
    markup = await confirm_edit_item_parameter_keyboard(item_id=data["item_id"], parameter=action)
    item = await select_item(data["item_id"])
    if action == "edit_item_name":
        await state.update_data(item_name=message.text)
        await message.answer(f"Новое наименование товара: {message.text}\n"
                             f"Подтвердить?",
                             reply_markup=markup)
    if action == "edit_item_description":
        await state.update_data(item_description=message.text)
        await message.answer(f"Новое описание товара: {message.text}\n"
                             f"Подтвердить?",
                             reply_markup=markup)
    if action == "edit_item_photo":
        await message.answer("Пробуем поймать фото")
        if message.content_type == "text":
            if message.text == "-":
                await state.update_data(item_photo=no_image_pic_url)
                await message.answer("Вы удаляете фото у товара.\n"
                                     "Подтвердить?",
                                     reply_markup=markup)
            else:
                await state.finish()  # если произошла ошибка валидации, то устанавливаем state = None
                await message.answer("Вы прислали некорректные данные.\n"
                                     "Чтобы повторить ввод, нажмите кнопку \"Прислать заново\"."
                                     "Если хотите отменить ввод, нажмите кнопку \"Отменить\".",
                                     reply_markup=await edit_item_repeat_input_or_cancel_keyboard(
                                         parameter="edit_item_photo",
                                         item_id=data["item_id"]))
        else:
            print("Определили фото")
            photo = message.photo[-1]
            uploaded_photo = await file_uploader.upload_photo(photo)
            await state.update_data(item_photo=uploaded_photo.link)
            await bot.send_photo(chat_id=message.chat.id,
                                 photo=uploaded_photo.link,
                                 caption="Новое фото товара загружено.\n"
                                         "Подтверить?",
                                 reply_markup=markup)
    if action == "edit_item_price":
        try:
            new_price = round(float(message.text), 2)
            await state.update_data(item_price=new_price)
            await message.answer(f"Новая стоимость товара: {new_price} RUB.\n"
                                 f"Подтвердить?",
                                 reply_markup=markup)
        except ValueError:
            await state.finish()  # если произошла ошибка валидации, то устанавливаем state = None
            await message.answer("Вы прислали некорректные данные.\n"
                                 "Чтобы повторить ввод, нажмите кнопку \"Прислать заново\"."
                                 "Если хотите отменить ввод, нажмите кнопку \"Отменить\".",
                                 reply_markup=await edit_item_repeat_input_or_cancel_keyboard(
                                     parameter="edit_item_price",
                                     item_id=data["item_id"]))
    if action == "edit_item_stock_quantity":
        print("action внутри условия action == edit_item_stock_quantity: ", action)
        try:
            new_item_quantity = int(message.text)
            await state.update_data(item_stock_quantity=new_item_quantity)
            await message.answer(f"Новое количество товара на складе: {new_item_quantity} {item.unit}\n"
                                 f"Подтвердить?",
                                 reply_markup=markup)
        except ValueError:
            await state.finish()  # если произошла ошибка валидации, то устанавливаем state = None
            await message.answer("Вы прислали некорректные данные.\n"
                                 "Чтобы повторить ввод, нажмите кнопку \"Прислать заново\"."
                                 "Если хотите отменить ввод, нажмите кнопку \"Отменить\".",
                                 reply_markup=await edit_item_repeat_input_or_cancel_keyboard(
                                     parameter="edit_item_stock_quantity",
                                     item_id=data["item_id"]))


@dp.callback_query_handler(text_startswith="confirm_edit_item_", state="confirm_edit_item_parameter")
async def call_edit_item_parameter(call: CallbackQuery, state: FSMContext):
    # await call.message.edit_reply_markup(reply_markup=None)
    action = call.data.split(":")[0]
    item_id = int(call.data.split(":")[1])
    data = await state.get_data()
    markup = await continue_edit_item_keyboard(item_id)
    item = await select_item(item_id)
    # await state.finish()
    if action == "confirm_edit_item_name":
        await update_item(item_id=item_id, param="name", value=data["item_name"])
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer(f"Новое наименование товара: {data['item_name']}.\n"
                                  f"Данные о товаре обновлены успешно.", reply_markup=markup)
        await state.finish()
    if action == "confirm_edit_item_description":
        await update_item(item_id=item_id, param="description", value=data["item_description"])
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer(f"Новое описание товара: {data['item_description']}.\n"
                                  f"Данные о товаре обновлены успешно.", reply_markup=markup)
        await state.finish()
    if action == "confirm_edit_item_photo":
        await update_item(item_id=item_id, param="photo", value=data["item_photo"])
        await call.message.edit_reply_markup(reply_markup=None)
        await bot.send_photo(chat_id=call["message"]["chat"]["id"],
                             photo=data["item_photo"],
                             caption="Вы успешно изменили фото товара.",
                             reply_markup=await edit_item_keyboard_data(item_id=item_id))
        await state.finish()
    if action == "confirm_edit_item_price":
        await update_item(item_id=item_id, param="price", value=data["item_price"])
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer(f"Новая стоимость товара: {data['item_price']} RUB.\n"
                                  f"Данные о товаре обновлены успешно.", reply_markup=markup)
        await state.finish()
    if action == "confirm_edit_item_stock_quantity":
        await update_item(item_id=item_id, param="stock_quantity", value=data["item_stock_quantity"])
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer(f"Новое количество товара на складе: {data['item_stock_quantity']} {item.unit}\n"
                                  f"Данные о товаре обновлены успешно.", reply_markup=markup)
        await state.finish()
    if action == "confirm_edit_item_unit":
        await update_item(item_id=item_id, param="unit", value=data["item_unit"])
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer(f"Новые единицы измерения товара: {data['item_unit']}\n"
                                  f"Данные о товаре обновлены успешно.", reply_markup=markup)
        await state.finish()
    if action == "confirm_edit_item_status":
        await update_item(item_id=item_id, param="status", value=data["item_status"])
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer(f"Новые статус товара: {data['item_status']}\n"
                                  f"Данные о товаре обновлены успешно.", reply_markup=markup)
        await state.finish()


@dp.callback_query_handler(text_startswith="continue_edit_item")
async def show_item_continue_edit(call: CallbackQuery, state: FSMContext):
    item_id = int(call.data.split(":")[1])
    print("call: ", call)
    print("call: ", call["message"]["chat"]["id"])
    print("item_id: ", item_id)
    item = await select_item(item_id)
    if call.from_user.id in admins:
        text = f"Наименование: {item.name}\n" \
               f"Описание: {item.description}\n" \
               f"Стоимость: {item.price} RUB\n" \
               f"Количество на складе: {item.stock_quantity} {item.unit}\n" \
               f"Статус товара: {item.status}"
    else:
        text = f"Наименование: {item.name}\n" \
               f"Описание: {item.description}\n" \
               f"Стоимость: {item.price} RUB\n" \
               f"Количество на складе: {item.stock_quantity} {item.unit}\n" \
               f"Статус товара: {item.status}"

    # await state.set_state("show_item")
    await call.message.answer("Обработка хендлера, чтобы показать товар")
    await call.message.edit_reply_markup(reply_markup=None)
    print("call.chat_instance.id", call["message"]["chat"]["id"])
    print("state: ", await state.get_state())
    # await state.set_state("show_item_continue_edit")
    await bot.send_photo(chat_id=call["message"]["chat"]["id"],
                         photo=item.photo,
                         caption=text,
                         reply_markup=await edit_item_keyboard_data(item_id=item_id))
