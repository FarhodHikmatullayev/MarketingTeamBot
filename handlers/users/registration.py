import datetime

import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import GROUP_CHAT_ID
from keyboards.default.menu import back_menu
from keyboards.inline.registration import registration_inline_keyboard, registration_callback_data
from loader import dp, db, bot


@dp.message_handler(text="Keldi-ketdi registratsiya", state='*')
async def start_registration(message: types.Message, state: FSMContext):
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

    await state.finish()
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    user = users[0]
    user_id = user['id']
    status = await db.select_status(user_id=user_id)
    at_work = status[0]['at_work']
    markup = await registration_inline_keyboard(user_id=user_id, at_work=at_work)
    text = "Registratsiya uchun tugmani bosing"
    await message.answer(text=text, reply_markup=markup)


@dp.callback_query_handler(registration_callback_data.filter())
async def on_off_status(call: types.CallbackQuery, callback_data=dict):
    on_off = callback_data.get('on_off')
    user_id = int(callback_data.get('user_id'))
    schedules = await db.select_schedules(user_id=user_id)
    status = await db.select_status(user_id=user_id)
    status = status[0]
    registrations_arrival = await db.get_today_registrations_for_user_by_arrival_time(user_id=user_id)
    registrations_departure = await db.get_today_registrations_for_user_by_departure_time(user_id=user_id)
    if on_off == 'on' and registrations_arrival:
        registration = registrations_arrival[0]
        arrival_time = registration['arrival_time']
        txt = f"Siz bugun {(arrival_time + datetime.timedelta(hours=5)).strftime('%d.%m.%Y, %H:%M')} da ishga kelganingizni tasdiqlagansiz"

    elif on_off == 'on':
        status = await db.update_status(id=status['id'], user_id=user_id, at_work=True)
        registration = await db.create_registration(
            user_id=user_id,
            arrival_time=datetime.datetime.now()
        )
        text = f"💼 {call.from_user.full_name} {(datetime.datetime.now()).strftime('%d.%m.%Y, %H:%M')} da ishga keldi"
        if schedules:
            schedule = schedules[0]
            text += f"\nIsh vaqti: {schedule['arrival_time']} - {schedule['departure_time']}"
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=text)
        # await bot.send_message(chat_id=call.message.chat.id, text=text)
        txt = "Siz ishga kelganingizni tasdiqladingiz"

    elif on_off == 'off' and registrations_departure:
        registration = registrations_departure[0]
        departure_time = registration['departure_time']
        txt = f"Siz bugun {(departure_time + datetime.timedelta(hours=5)).strftime('%d.%m.%Y, %H:%M')} da ishdan ketganingizni tasdiqlagansiz"

    elif on_off == 'off' and not registrations_arrival:
        status = await db.update_status(id=status['id'], user_id=user_id)
        text = f"🏠 {call.from_user.full_name} {(datetime.datetime.now() + datetime.timedelta(hours=5)).strftime('%d.%m.%Y, %H:%M')} da ishdan ketdi\n"
        if schedules:
            schedule = schedules[0]
            text += f"\nIsh vaqti: {schedule['arrival_time']} - {schedule['departure_time']}"
        txt = "Ishdan ketganingizni tasdiqladingiz"
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=text)
        # await bot.send_message(chat_id=call.message.chat.id, text=text)

    elif on_off == 'off':
        status = await db.update_status(id=status['id'], user_id=user_id)

        total_time = datetime.datetime.now(pytz.timezone('Asia/Tashkent')) - registrations_arrival[0]['arrival_time']
        total_seconds = int(total_time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        registration = await db.update_registration(
            id=registrations_arrival[0]['id'],
            user_id=user_id,
            arrival_time=registrations_arrival[0]['arrival_time'],
            departure_time=datetime.datetime.now(),
            total_time=total_time,
        )
        text = f"🏠 {call.from_user.full_name} {(datetime.datetime.now()).strftime('%d.%m.%Y, %H:%M')} da ishdan ketdi\n" \
               f"Umumiy {hours} soat {minutes} daqiqa vaqt ishladi"
        if schedules:
            schedule = schedules[0]
            text += f"\nIsh vaqti: {schedule['arrival_time']} - {schedule['departure_time']}"
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=text)
        # await bot.send_message(chat_id=call.message.chat.id, text=text)
        txt = "Ishdan ketganingizni tasdiqladingiz"
    await call.message.answer(text=txt, reply_markup=back_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
