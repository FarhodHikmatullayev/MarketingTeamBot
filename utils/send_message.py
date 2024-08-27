from data.config import ADMINS
from loader import bot
import logging


async def send_message_to_admins(message):
    for admin in ADMINS:
        try:
            await bot.send_message(admin, message)
        except Exception as err:
            logging.exception(err)
