from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

registration_callback_data = CallbackData('registration', 'user_id', 'on_off')


async def registration_inline_keyboard(user_id, at_work):
    if not at_work:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Keldim",
                        callback_data=registration_callback_data.new(user_id=user_id, on_off='on')
                    ),
                ]
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Ketdim",
                    callback_data=registration_callback_data.new(user_id=user_id, on_off='off')
                ),
            ]
        ]
    )
