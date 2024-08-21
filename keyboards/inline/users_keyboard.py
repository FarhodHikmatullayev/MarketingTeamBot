from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db

users_callback_data = CallbackData('users', 'user_id')


async def users_inline_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    users = await db.select_all_users()
    buttons = []
    for user in users:
        callback_data = users_callback_data.new(user_id=user['id'])
        buttons.append(
            InlineKeyboardButton(
                text=user['full_name'],
                callback_data=callback_data
            )
        )
    if buttons:
        markup.add(*buttons)
    return markup
