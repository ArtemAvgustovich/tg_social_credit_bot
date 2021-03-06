""" Run a function by ado <func_name> """


def set_hook():
    import asyncio
    from bot.settings import HEROKU_APP_NAME, WEBHOOK_URL, TOKEN
    from aiogram import Bot
    bot = Bot(token=TOKEN)
    
    async def hook_set():
        if not HEROKU_APP_NAME:
            print('You have forgot to set HEROKU_APP_NAME')
            quit()
        await bot.set_webhook(WEBHOOK_URL)
        print(await bot.get_webhook_info())
    
    asyncio.run(hook_set())
    bot.close()


def start():
    from bot.bot import main
    from database import setup_table
    setup_table()
    main()


if __name__ == '__main__':
    start()
