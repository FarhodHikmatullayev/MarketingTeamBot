from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS, GROUP_CHAT_ID
from keyboards.default.back_users import back_or_save_keyboard
from keyboards.default.menu import back_menu
from keyboards.inline.users_keyboard import users_inline_keyboard, users_callback_data
from loader import dp, db, bot
from states.warnings import WarningState


@dp.message_handler(text="Ogohlantirishlar", user_id=ADMINS, state='*')
async def get_users(message: types.Message, state: FSMContext):
    await state.finish()
    text = "Xodimlardan birini tanlang"
    markup = await users_inline_keyboard()
    await message.answer(text=text, reply_markup=markup)


@dp.message_handler(text="Ogohlantirishlar", state='*')
async def send_warning(message: types.Message, state: FSMContext):
    await state.finish()
    text = "Siz admin emassiz\n" \
           "Sizda ogohlantirish berish uchun ruhsat mavjud emas"
    await message.answer(text=text)


@dp.callback_query_handler(users_callback_data.filter())
async def start_making_warning(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_telegram_id = call.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    warned_by_id = users[0]['id']

    user_id = callback_data.get('user_id')

    await state.update_data(
        {
            'user_id': user_id,
            'warned_by_id': warned_by_id
        }
    )

    text = "Ogohlantirish matnini kiriting"

    await call.message.edit_text(text=text)
    await WarningState.text.set()


@dp.message_handler(text="Orqaga", state=WarningState.text)
async def save_warning(msg: types.Message, state: FSMContext):
    text = "Xodimlardan birini tanlang"
    markup = await users_inline_keyboard()
    await msg.answer(text=text, reply_markup=markup)
    await state.finish()


@dp.message_handler(text="Saqlash", state=WarningState.text)
async def save_warning(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = int(data.get('user_id'))
    warned_by_id = int(data.get('warned_by_id'))
    txt = data.get('text')

    warning = await db.create_warning(
        user_id=user_id,
        text=txt,
        warned_by_id=warned_by_id
    )
    users = await db.select_users(id=user_id)
    user = users[0]
    warned_users = await db.select_users(id=warned_by_id)
    warned_user = warned_users[0]

    text = f"@{user['username']} Sizga ogohlantirish berildi\n" \
           f"Izoh: {txt}\n" \
           f"{warned_user['full_name']}"

    await bot.send_message(chat_id=GROUP_CHAT_ID, text=text)

    text = "Muvaffaqiyatli saqlandi"
    await msg.answer(text=text, reply_markup=back_menu)
    await state.finish()


@dp.message_handler(state=WarningState.text)
async def create_warning(msg: types.Message, state: FSMContext):
    txt = msg.text
    await state.update_data(
        {
            'text': txt
        }
    )
    text = ""
    text += f"Ogohlantirish: {txt}"
    await msg.answer(text=text)
    await msg.answer(
        text="Saqlashni xohlaysizmi?",
        reply_markup=back_or_save_keyboard
    )
