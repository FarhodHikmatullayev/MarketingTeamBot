from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db

application_callback_data = CallbackData('application', 'id')
application_confirm_callback_data = CallbackData('confirm', 'application_id', 'confirmation')


async def applications_keyboard(*applications):
    markup = InlineKeyboardMarkup()
    buttons = []
    for application in applications:
        application = application[0]
        user_id = application['user_id']
        users = await db.select_users(id=user_id)
        user_full_name = users[0]['full_name']
        # username = users[0]['username']
        callback_data = application_callback_data.new(id=application['id'])
        buttons.append(
            InlineKeyboardButton(
                text=f"{user_full_name}",
                callback_data=callback_data
            )
        )
    if buttons:
        markup.add(*buttons)
    return markup


async def confirmation_markup(application_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Tasdiqlash",
                    callback_data=application_confirm_callback_data.new(
                        application_id=application_id,
                        confirmation="confirm"
                    )
                ),
                InlineKeyboardButton(
                    text="Rad etish",
                    callback_data=application_confirm_callback_data.new(
                        application_id=application_id,
                        confirmation="reject"
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="Orqaga",
                    callback_data=application_confirm_callback_data.new(
                        application_id=application_id,
                        confirmation="back"
                    )
                )
            ]
        ]
    )
    return markup
