from aiogram import types

from data.config import ADMINS
from keyboards.default.menu import back_menu
from loader import dp, db


@dp.message_handler(text="Xodimlar statusi")
async def get_users(message: types.Message):
    all_status = await db.select_all_status()
    if not all_status:
        text = "Hali xodimlarning statuslari mavjud emas"
        await message.answer(text=text, reply_markup=back_menu)
    else:
        text = ""
        tr = 0
        for status in all_status:
            tr += 1

            user_id = status['user_id']
            at_work = status['at_work']
            users = await db.select_users(id=user_id)
            user = users[0]
            user_full_name = user['full_name']
            username = user['username']
            if at_work:
                if user_full_name:
                    text += f"{tr}. {user_full_name}  ✔️\n"
                else:
                    text += f"{tr}. {username}  ✔️\n"
            else:
                if user_full_name:
                    text += f"{tr}. {user_full_name}  ❌\n"
                else:
                    text += f"{tr}. {username}  ❌\n"

        await message.answer(text=text, reply_markup=back_menu)
