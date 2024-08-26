import datetime

import pytz
from aiogram import types

from data.config import GROUP_CHAT_ID
from keyboards.default.menu import back_menu
from keyboards.inline.registration import registration_inline_keyboard, registration_callback_data
from loader import dp, db, bot


@dp.message_handler(text="Keldi-ketdi registratsiya")
async def start_registration(message: types.Message):
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
    status = await db.select_status(user_id=user_id)
    status = status[0]
    registrations_arrival = await db.get_today_registrations_for_user_by_arrival_time(user_id=user_id)
    registrations_departure = await db.get_today_registrations_for_user_by_departure_time(user_id=user_id)
    if on_off == 'on' and registrations_arrival:
        registration = registrations_arrival[0]
        arrival_time = registration['arrival_time'].time()
        txt = f"Siz bugun {arrival_time} da ishga kelganingizni tasdiqlagansiz"

    elif on_off == 'on':
        status = await db.update_status(id=status['id'], user_id=user_id, at_work=True)
        registration = await db.create_registration(
            user_id=user_id,
            arrival_time=datetime.datetime.now()
        )
        text = f"💼 {call.from_user.full_name} {(datetime.datetime.now() + datetime.timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')} da ishga keldi"
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=text)
        # await bot.send_message(chat_id=call.message.chat.id, text=text)
        txt = "Siz ishga kelganingizni tasdiqladingiz"

    elif on_off == 'off' and registrations_departure:
        registration = registrations_departure[0]
        departure_time = registration['departure_time'].time()
        txt = f"Siz bugun {departure_time} da ishdan ketganingizni tasdiqlagansiz"

    elif on_off == 'off' and not registrations_arrival:
        status = await db.update_status(id=status['id'], user_id=user_id)
        text = f"🏠 {call.from_user.full_name} {(datetime.datetime.now() + datetime.timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')} da ishdan ketdi\n"
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
        text = f"🏠 {call.from_user.full_name} {(datetime.datetime.now() + datetime.timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')} da ishdan ketdi\n" \
               f"Umumiy {hours} soat {minutes} daqiqa vaqt ishladi"
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=text)
        # await bot.send_message(chat_id=call.message.chat.id, text=text)
        txt = "Ishdan ketganingizni tasdiqladingiz"
    await call.message.answer(text=txt, reply_markup=back_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
