from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp, db


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):

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

    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam")

    await message.answer("\n".join(text))
