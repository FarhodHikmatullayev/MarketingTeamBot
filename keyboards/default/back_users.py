from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

back_or_save_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Orqaga"),
            KeyboardButton(text="Saqlash")
        ]
    ]
)
