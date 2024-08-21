import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.back_users import back_or_save_keyboard
from keyboards.default.menu import back_menu, menu_keyboard
from keyboards.inline.applications_keyboards import applications_keyboard, application_callback_data, \
    confirmation_markup, application_confirm_callback_data
from loader import dp, db, bot
from states.applications import ApplicationState


@dp.message_handler(text="Dam olish so'rash")
async def ask_for(message: types.Message, state: FSMContext):
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    user_id = users[0]['id']

    await state.update_data(
        {
            'user_id': user_id,
            'is_confirmed': False,
        }
    )

    text = "Nega javob olmoqchisiz? \n" \
           "Sababini yozing"
    await message.answer(text=text)
    await state.set_state(ApplicationState.description.state)


@dp.message_handler(text="Orqaga", state=ApplicationState.description)
async def back_main_menu(msg: types.Message, state: FSMContext):
    await state.finish()
    text = "Quyidagi bo'limlardan birini tanlang"
    markup = await menu_keyboard(user_id=msg.from_user.id)
    await msg.answer(text=text, reply_markup=markup)


@dp.message_handler(text="Saqlash", state=ApplicationState.description)
async def save_warning(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = int(data.get('user_id'))
    description = data.get('description')
    is_confirmed = data.get('is_confirmed')

    application = await db.create_application(
        user_id=user_id,
        description=description
    )
    text = "Muvaffaqiyatli saqlandi"
    await msg.answer(text=text, reply_markup=back_menu)
    await state.finish()


@dp.message_handler(state=ApplicationState.description)
async def get_description_for_application(message: types.Message, state: FSMContext):
    txt = message.text
    await state.update_data(
        {
            'description': txt
        }
    )

    text = "Sizning arizangiz: \n" \
           f"{txt}"
    await message.answer(text=text)

    text = "Arizangiz saqlansinmi?"
    await message.answer(text=text, reply_markup=back_or_save_keyboard)


@dp.message_handler(text="Dam olishga tushgan arizalar", user_id=ADMINS)
async def get_users(message: types.Message):
    all_applications = await db.select_all_applications()
    applications = []
    for i in all_applications:
        if not i['confirmed_by_id']:
            applications.append(i)
    if not applications:
        text = "Hali dam olish uchun arizalar mavjud emas"
        await message.answer(text=text, reply_markup=back_menu)

    else:
        text = "Arizalarni ko'rish uchun ulardan birini tanlang"
        markup = await applications_keyboard(applications)
        await message.answer(text=text, reply_markup=markup)


@dp.callback_query_handler(application_callback_data.filter())
async def see_applications(call: types.CallbackQuery, callback_data: dict):
    application_id = int(callback_data.get('id'))
    applications = await db.select_applications(id=application_id)
    application = applications[0]
    created_time = application['created_at'] + datetime.timedelta(hours=5)
    user_id = application['user_id']
    users = await db.select_users(id=user_id)
    user = users[0]
    text = ""
    text += f"Ariza egasi: {user['full_name']}\n"
    text += f"Ariza sababi: {application['description']}\n"
    text += f"Vaqt: {created_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    markup = await confirmation_markup(application['id'])
    await call.message.edit_text(text=text)
    await call.message.answer(text="Ruxsat berasizmi?", reply_markup=markup)


@dp.callback_query_handler(application_confirm_callback_data.filter())
async def confirm_or_reject_application(call: types.CallbackQuery, callback_data: dict):
    confirmation = callback_data.get('confirmation')
    application_id = int(callback_data.get('application_id'))
    if confirmation == "back":
        all_applications = await db.select_all_applications()
        applications = []
        for i in all_applications:
            if not i['confirmed_by_id']:
                applications.append(i)
        if not applications:
            text = "Hali dam olish uchun arizalar mavjud emas"
            await call.message.answer(text=text, reply_markup=back_menu)

        else:
            text = "Arizalarni ko'rish uchun ulardan birini tanlang"
            markup = await applications_keyboard(applications)
            await call.message.answer(text=text, reply_markup=markup)

    elif confirmation == 'reject':
        users = await db.select_users(telegram_id=call.from_user.id)
        user = users[0]
        await db.update_application(
            id=application_id,
            confirmed_by_id=user['id']
        )
        text = "Siz arizani rad etdingiz"
        await call.message.answer(text=text, reply_markup=back_menu)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif confirmation == 'confirm':
        users = await db.select_users(telegram_id=call.from_user.id)
        user = users[0]
        await db.update_application(
            id=application_id,
            confirmed_by_id=user['id'],
            is_confirmed=True
        )
        text = "Siz arizani tasdiqladingiz"
        await call.message.answer(text=text, reply_markup=back_menu)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
