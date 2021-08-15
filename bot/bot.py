# *-* encoding utf-8
import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from constants import add_rating_sticker_id, remove_rating_sticker_id
from settings import TOKEN, WEBHOOK_PATH, WEBAPP_PORT, WEBAPP_HOST, WEBHOOK_URL

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Poshel nahui")


@dp.message_handler(content_types=types.ContentType.STICKER)
async def add_rating(message: types.Message):
    """
    :param message:
    :return:
    """
    
    sticker = message.sticker
    if not sticker.set_name == 'PoohSocialCredit':
        await message.reply("Unknown sticker")
        return
    if message.reply_to_message is not None:
        user_to_change_rating = message.reply_to_message.from_user
        if sticker.file_unique_id == add_rating_sticker_id:
            await message.reply(f"{message.from_user.username} added 20 social credit to {user_to_change_rating.username}")
        elif sticker.file_unique_id == remove_rating_sticker_id:
            await message.reply(f"{message.from_user.username} removed 20 social from to {user_to_change_rating.username}")
        else:
            await message.reply(str(vars(sticker)))
    else:
        await message.reply("It seems like you forgot to reply")


async def on_startup(dispatcher):
    logging.warning("Starting connection.")
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    logging.warning("Bye! Shutting down webhook connection")


def main():
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )