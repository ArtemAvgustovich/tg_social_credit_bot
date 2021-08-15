import os


TOKEN = os.getenv('TOKEN')
if not TOKEN:
    print("You have forgot to set TOKEN")
    quit()

HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")


# webhook settings
WEBHOOK_HOST = f"https://{HEROKU_APP_NAME}.herokuapp.com"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT"))
