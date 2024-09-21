from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.menu import menu_keyboard
from loader import dp, db


@dp.message_handler(text="Asosiy menyuga qaytish", state='*')
async def send_warning(message: types.Message, state: FSMContext):
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
    markup = await menu_keyboard(user_id=message.from_user.id)
    await message.answer(text="Quyidagi bo'limlardan birini tanlang", reply_markup=markup)
