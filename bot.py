# *-* encoding utf-8
import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from constants import add_rating_sticker_id, remove_rating_sticker_id

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=os.environ.get('TOKEN'))
dp = Dispatcher(bot)


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
        return
    if message.reply_to_message is not None:
        user_to_change_rating = message.reply_to_message.from_user
        if sticker.file_unique_id == add_rating_sticker_id:
            await message.reply(f"{message.from_user.username} added 20 social credit to {user_to_change_rating.username}")
        elif sticker.file_unique_id == remove_rating_sticker_id:
            await message.reply(f"{message.from_user.username} removed 20 social from to {user_to_change_rating.username}")
    else:
        await message.reply("It seems like you forgot to reply")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
