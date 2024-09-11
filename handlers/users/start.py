import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.default.contakt_button import keyboard
from keyboards.default.menu import menu_keyboard
from loader import dp, db, bot


@dp.message_handler(content_types='contact')
async def get_contact(message: Message):
    contact = message.contact

    try:
        user = await db.create_user(phone=contact.phone_number, telegram_id=message.from_user.id,
                                    username=message.from_user.username, full_name=message.from_user.full_name)
        user_status = await db.create_status(user_id=user['id'])
        await message.answer(f"Rahmat, <b>{contact.full_name}</b>.\n"
                             f"Sizning {contact.phone_number} raqamingizni qabul qildik.",
                             reply_markup=ReplyKeyboardRemove())
        markup = await menu_keyboard(user_id=message.from_user.id)
        await message.answer(text="Endi quyidagi bo'limlardan birini tanlang", reply_markup=markup)

    except asyncpg.exceptions.UniqueViolationError:
        user_telegram_id = message.from_user.id
        users = await db.select_users(telegram_id=user_telegram_id)
        user = users[0]
        status = await db.select_status(user_id=user['id'])
        if not status:
            user_status = await db.create_status(user_id=user['id'])
        text = "Siz allaqachon ro'yxatdan o'tgan ekansiz\n" \
               "Endi quyidagi bo'limlardan birini tanlang"
        markup = await menu_keyboard(user_id=message.from_user.id)
        await message.answer(text=text, reply_markup=markup)


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    print('user_telegram_id', message.from_user.id)
    users = await db.select_users(telegram_id=message.from_user.id)
    # await bot.send_message(chat_id=-1002210692356, text="chat_id_topildi")
    if not users:
        text = f"Salom, {message.from_user.full_name}!\n"
        text += "Botimizga xush kelibsiz\n" \
                "Botdan ro'yxatdan o'tish uchun kontaktingizni yuboring"

        await message.answer(text, reply_markup=keyboard)
    else:
        text = f"Salom, {message.from_user.full_name}!\n"
        text += "Botimizga xush kelibsiz\n" \
                "Quyidagi bo'limlardan birini tanlang"
        markup = await menu_keyboard(user_id=message.from_user.id)
        await message.answer(text=text, reply_markup=markup)
    await state.finish()
