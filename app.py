from aiogram import executor

from data.config import DEVELOPMENT_MODE, BOT_TOKEN
from keep_alive import keep_alive
from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

if not DEVELOPMENT_MODE:
    keep_alive()


async def on_startup(dispatcher):
    await db.create()
    # await bot.set_webhook(WEBHOOK_URL)

    await set_default_commands(dispatcher)

    # await on_startup_notify(dispatcher)


#
# WEBHOOK_HOST = 'https://tbandtxbot.onrender.com'
# WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
# WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
