from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.menu import menu_keyboard, back_menu

from keyboards.inline.confirmation import confirm_keyboard, confirmation_for_edit_or_delete, \
    confirmation_for_edit_or_delete_without_back_button
from keyboards.inline.users_keyboard import users_callback_data1, users_inline_keyboard1

from loader import dp, db, bot
from states.schedules import ScheduleCreateState, ScheduleUpdateState


@dp.message_handler(text="Ish grafiklari", user_id=ADMINS, state='*')
async def get_users(message: types.Message, state: FSMContext):
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        await message.answer(text="Sizda botdan foydalanish uchun ruxsat mavjud emas!")
        return
    else:
        user = users[0]
        user_is_active = user['is_active']
        if not user_is_active:
            await message.answer(text="Sizda botdan foydalanish uchun ruxsat mavjud emas!")
            return

    await ScheduleUpdateState.user_id.set()
    text = "Xodimlardan birini tanlang"
    markup = await users_inline_keyboard1()
    await message.answer(text=text, reply_markup=markup)


@dp.message_handler(text="Ish grafiklari", state='*')
async def get_user(message: types.Message, state: FSMContext):
    await state.finish()
    text = "Siz admin emassiz\n" \
           "Sizga bu funksiyadan foydalanishda ruxsat mavjud emas"
    await message.answer(text=text)


@dp.callback_query_handler(users_callback_data1.filter(), state=ScheduleUpdateState.user_id)
async def start_making_warning(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_telegram_id = call.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)

    user_id = int(callback_data.get('user_id'))

    users = await db.select_users(id=user_id)
    schedules = await db.select_schedules(user_id=user_id)
    if not schedules:
        await call.message.edit_text(f"{users[0]['full_name']} uchun ish grafigi belgilanmagan")
        await call.message.answer(text="Ish grafigi yaratasizmi?", reply_markup=confirm_keyboard)
        await ScheduleCreateState.user_id.set()

    else:
        await call.message.edit_text(f"{users[0]['full_name']} ning ish grafigi:\n"
                                     f"Kelish vaqti: {schedules[0]['arrival_time']}\n"
                                     f"Ketish vaqti: {schedules[0]['departure_time']}\n")
        await call.message.answer("O'zgartirishni yoki o'chirishni xohlaysizmi",
                                  reply_markup=confirmation_for_edit_or_delete)

    await state.update_data(
        {
            'user_id': user_id,
        }
    )


@dp.callback_query_handler(text="back", state=ScheduleUpdateState.user_id)
async def back_to_schedules(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    text = "Xodimlardan birini tanlang"
    markup = await users_inline_keyboard1()
    await call.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(text='delete', state=ScheduleUpdateState.user_id)
async def delete_user_schedule(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    schedules = await db.select_schedules(user_id=user_id)
    schedule = schedules[0]
    schedule_id = schedule['id']

    await db.delete_schedule(id=schedule_id)

    await call.message.answer(text="Ish jadvali muvaffaqiyatli o'chirildi", reply_markup=back_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    await state.finish()


@dp.callback_query_handler(text="edit", state=ScheduleUpdateState.user_id)
async def start_editing_schedule(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    users = await db.select_users(id=user_id)
    user = users[0]
    user_full_name = user['full_name']

    text = f"{user_full_name} uchun kelish vaqtini kiriting: \nMisol: 8:30"

    await call.message.answer(text=text, reply_markup=back_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await ScheduleUpdateState.arrival_time.set()


@dp.message_handler(state=ScheduleUpdateState.arrival_time)
async def get_arrival_time(message: types.Message, state: FSMContext):
    arrival_time = message.text
    await state.update_data(arrival_time=arrival_time)
    await ScheduleUpdateState.departure_time.set()
    await message.answer(text="Ketish vaqtini kiriting", reply_markup=back_menu)


@dp.message_handler(state=ScheduleUpdateState.departure_time)
async def get_departure_time(message: types.Message, state: FSMContext):
    departure_time = message.text
    await state.update_data(departure_time=departure_time)
    data = await state.get_data()
    user_id = data.get("user_id")
    users = await db.select_users(id=user_id)
    user = users[0]
    user_full_name = user['full_name']
    arrival_time = data.get("arrival_time")
    text = (f"{user_full_name} uchun ish grafigi:\n"
            f"Kelish vaqti: {arrival_time}\n"
            f"Ketish vaqti: {departure_time}")
    await message.answer(text=text)
    await message.answer(text="Saqlashni xohlaysizmi", reply_markup=confirm_keyboard)


@dp.callback_query_handler(text='no', state=ScheduleCreateState.user_id)
async def confirm_creating_schedule(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    markup = await menu_keyboard(user_id=call.from_user.id)
    await call.message.answer(text="Quyidagi bo'limlardan birini tanlang", reply_markup=markup)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text='yes', state=ScheduleCreateState.user_id)
async def confirm_creating_schedule(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    await call.message.answer(text="Xodimning kelish vaqtini kiriting: \nMisol: 08:20", reply_markup=back_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await ScheduleCreateState.arrival_time.set()


@dp.message_handler(state=ScheduleCreateState.arrival_time)
async def get_arrival_time(message: types.Message, state: FSMContext):
    arrival_time = message.text
    await state.update_data(arrival_time=arrival_time)
    await message.answer(text="Ketish vaqtini kiriting:", reply_markup=back_menu)
    await ScheduleCreateState.departure_time.set()


@dp.message_handler(state=ScheduleCreateState.departure_time)
async def get_departure_time(message: types.Message, state: FSMContext):
    departure_time = message.text
    await state.update_data(departure_time=departure_time)
    data = await state.get_data()
    user_id = data.get('user_id')
    arrival_time = data.get('arrival_time')
    users = await db.select_users(id=user_id)
    user = users[0]
    user_full_name = user['full_name']

    text = (f"{user_full_name} uchun ish grafigi:\n"
            f"Kelish vaqti: {arrival_time}\n"
            f"Ketish vaqti: {departure_time}")
    await message.answer(text=text)
    await message.answer(text="Saqlashni xohlaysizmi", reply_markup=confirm_keyboard)


@dp.callback_query_handler(text='no',
                           state=[ScheduleCreateState.departure_time, ScheduleUpdateState.departure_time])
async def cancel_creating_schedule(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer(text="Saqlash rad etildi", reply_markup=back_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text='yes', state=ScheduleCreateState.departure_time)
async def confirm_creating_schedule(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    arrival_time = data.get('arrival_time')
    departure_time = data.get('departure_time')

    schedule = await db.create_schedule(
        user_id=user_id,
        arrival_time=arrival_time,
        departure_time=departure_time
    )
    await call.message.answer(text="Muvaffaqiyatli saqlandi", reply_markup=back_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text='yes', state=ScheduleUpdateState.departure_time)
async def confirm_editing_schedule(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    arrival_time = data.get('arrival_time')
    departure_time = data.get('departure_time')
    schedules = await db.select_schedules(user_id=user_id)
    schedule = schedules[0]
    schedule_id = schedule['id']

    schedule = await db.update_schedule(
        id=schedule_id,
        arrival_time=arrival_time,
        departure_time=departure_time
    )
    await call.message.answer(text="Muvaffaqiyatli o'zgartirildi", reply_markup=back_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


# for users
@dp.message_handler(text="Ish grafigim", state='*')
async def get_users(message: types.Message, state: FSMContext):
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    if not users:
        await message.answer(text="Sizda botdan foydalanish uchun ruxsat mavjud emas!")
        return

    user = users[0]
    user_id = user['id']
    user_is_active = user['is_active']
    if not user_is_active:
        await message.answer(text="Sizda botdan foydalanish uchun ruxsat mavjud emas!")
        return
    await ScheduleUpdateState.user_id.set()
    await state.update_data(
        {
            'user_id': user_id,
        }
    )

    schedules = await db.select_schedules(user_id=user_id)
    if not schedules:
        await message.answer(text="Hali sizning ish grafigingiz kiritilmagan")
        await message.answer(text="Ish grafigi yaratasizmi?", reply_markup=confirm_keyboard)
        await ScheduleCreateState.user_id.set()

    else:
        await message.answer(f"Sizning ish grafigingiz:\n"
                                f"Kelish vaqti: {schedules[0]['arrival_time']}\n"
                                f"Ketish vaqti: {schedules[0]['departure_time']}\n")
        await message.answer("O'zgartirishni yoki o'chirishni xohlaysizmi",
                             reply_markup=confirmation_for_edit_or_delete_without_back_button)
