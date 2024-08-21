import datetime

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
    markup = await registration_inline_keyboard(user_id=user_id)
    text = "Registratsiya uchun tugmani tanlang"
    await message.answer(text=text, reply_markup=markup)


@dp.callback_query_handler(registration_callback_data.filter())
async def on_off_status(call: types.CallbackQuery, callback_data=dict):
    on_off = callback_data.get('on_off')
    user_id = int(callback_data.get('user_id'))
    status = await db.select_status(user_id=user_id)
    status = status[0]
    if on_off == 'on':
        status = await db.update_status(id=status['id'], user_id=user_id, at_work=True)

        text = f"{call.from_user.full_name} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} da ishga keldi"
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=text)

    elif on_off == 'off':
        status = await db.update_status(id=status['id'], user_id=user_id)

        text = f"{call.from_user.full_name} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} da ishdan ketdi"
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=text)

    text = "Muvaffaqiyatli registratsiyadan o'tildi"
    await call.message.answer(text=text, reply_markup=back_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
