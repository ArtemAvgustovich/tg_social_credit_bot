# *-* encoding utf-8
import logging
import random
from time import time

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from bot.constants import add_rating_sticker_id, remove_rating_sticker_id, HELP_MESSAGE, DO_NOT_CHANGE_MY_RATING, \
    timeout_table, add_rating_timeout
from bot.settings import TOKEN, WEBHOOK_PATH, WEBAPP_PORT, WEBAPP_HOST, WEBHOOK_URL
from database import change_rating, chat_stats


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
    await message.reply(HELP_MESSAGE)


@dp.message_handler(commands=['social_rating'])
async def show_rating_stats(message: types.Message):
    ranks = sorted(chat_stats(message.chat.id), key=lambda x: -x[1])
    await message.reply("\n".join(f"{username} {rating}" for username, rating in ranks))


@dp.message_handler(content_types=types.ContentType.STICKER)
async def process_sticker(message: types.Message):
    logging.info(f"[process_sticker] Processing sticker ({message.sticker.set_name}, {message.sticker.emoji})")
    if message.sticker.set_name == 'PoohSocialCredit':
        await change_social_rating(message)


async def on_startup(dispatcher):
    logging.warning("Starting connection.")
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    logging.warning("Bye! Shutting down webhook connection")


async def can_change_rating(message, affected_user):
    logging.debug(f"[can_change_rating] affected_user_id = {affected_user.id}, sender_id = {message.from_user.id}")
    
    now = time()
    timeout = int(timeout_table.get(message.chat.id, {}).get(affected_user.id, 0) - now)
    me = await bot.me
    
    if affected_user.id == me.id:
        message.reply(random.choice(DO_NOT_CHANGE_MY_RATING))
        return False
    elif affected_user.is_bot:
        message.reply("Can't edit bot's social rating credit!")
        return False
    elif affected_user.id == message.from_user.id:
        message.reply("Can't edit self social rating credit!")
        return False
    elif timeout > 0:
        message.reply(f"You can't edit {affected_user.username}'s social rating credit for {timeout} seconds!")
        return False
    timeout_table.setdefault(message.chat.id, {})[affected_user.id] = now + add_rating_timeout
    return True


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
    
    can_change = await can_change_rating(message, affected_user)
    if can_change:
        logging.info(f"[change_social_rating] {username}'s rating changed by {sender_username}.\n"
                     f"user_id: {user_id}, chat_id: {chat_id}")
        if sticker.file_unique_id == add_rating_sticker_id:
            new_rating = change_rating(user_id, chat_id, username, 20)
            await message.reply(f"{sender_username} added 20 social rating credit to {username}\n"
                                f"Now his rating is {new_rating}")
        elif sticker.file_unique_id == remove_rating_sticker_id:
            new_rating = change_rating(user_id, chat_id, username, -20)
            await message.reply(f"{sender_username} removed 20 social rating from to {username}\n"
                                f"Now his rating is {new_rating}")
        else:
            logging.warning(f"[change_social_rating] Unknown sticker ({sticker.set_name}, {sticker.emoji})")
    else:
        await message.reply(reply_message)


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