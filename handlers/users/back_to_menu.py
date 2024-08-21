from aiogram import types

from keyboards.default.menu import menu_keyboard
from loader import dp


@dp.message_handler(text="Asosiy menyuga qaytish")
async def send_warning(message: types.Message):
    markup = await menu_keyboard(user_id=message.from_user.id)
    await message.answer(text="Quyidagi bo'limlardan birini tanlang", reply_markup=markup)
