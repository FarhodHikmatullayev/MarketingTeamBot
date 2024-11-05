from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.config import ADMINS

back_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Asosiy menyuga qaytish")
        ]
    ]
)


async def menu_keyboard(user_id):
    if str(user_id) in ADMINS:

        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text='Xodimlar statusi'),
                    KeyboardButton(text='Ish grafiklari')
                ],
                [
                    KeyboardButton(text='Keldi-ketdi registratsiya')
                ],
                [
                    KeyboardButton(text='Dam olish so\'rash'),
                ],
                [
                    KeyboardButton(text='Ogohlantirishlar'),
                    KeyboardButton(text='Dam olishga tushgan arizalar'),
                ]
            ]
        )
    else:
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text='Xodimlar statusi'),
                    KeyboardButton(text='Keldi-ketdi registratsiya')
                ],
                [
                    KeyboardButton(text="Ish grafigim")
                ],
                [
                    KeyboardButton(text='Dam olish so\'rash'),
                ],
            ]
        )
