from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="yes"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data='no')
        ]
    ]
)

confirmation_for_edit_or_delete = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Edit', callback_data='edit'),
            InlineKeyboardButton(text='Delete', callback_data='delete'),
            InlineKeyboardButton(text='Back', callback_data='back'),
        ]
    ]
)

confirmation_for_edit_or_delete_without_back_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Edit', callback_data='edit'),
            InlineKeyboardButton(text='Delete', callback_data='delete'),
        ]
    ]
)
