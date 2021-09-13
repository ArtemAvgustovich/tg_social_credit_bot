# *-* encoding utf-8
import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from bot.constants import add_rating_sticker_id, remove_rating_sticker_id
from bot.settings import TOKEN, WEBHOOK_PATH, WEBAPP_PORT, WEBAPP_HOST, WEBHOOK_URL
from database import change_rating


# Configure logging
logging.basicConfig(level=logging.DEBUG)

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
async def process_sticker(message: types.Message):
    logging.info(f"[process_sticker] Processing sticker ({message.sticker.set_name}, {message.sticker.emoji})")
    if message.sticker.set_name == 'PoohSocialCredit':
        await change_social_rating(message)
    else:
        await message.reply("Unknown stickerpack")


async def on_startup(dispatcher):
    logging.warning("Starting connection.")
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    logging.warning("Bye! Shutting down webhook connection")


async def change_social_rating(message: types.Message):
    sender_username = message.from_user.username
    if message.reply_to_message is None:
        logging.debug(f"[change_social_rating] User {sender_username} didn't reply.")
        return

    affected_user = message.reply_to_message.from_user
    user_id = affected_user.id
    chat_id = message.chat.id
    sticker = message.sticker
    username = affected_user.username
    
    logging.info(f"[change_social_rating] {username}'s rating changed by {sender_username}. "
                 f"user_id: {user_id}, chat_id: {chat_id}")
    
    if sticker.file_unique_id == add_rating_sticker_id:
        change_rating(user_id, chat_id, username, 20)
        await message.reply(f"{sender_username} added 20 social rating credit to {username}")
    elif sticker.file_unique_id == remove_rating_sticker_id:
        change_rating(user_id, chat_id, username, -20)
        await message.reply(f"{sender_username} removed 20 social rating from to {username}")
    else:
        logging.warning(f"[change_social_rating] Unknown sticker ({sticker.set_name}, {sticker.emoji})")


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