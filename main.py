import os
from telegram.ext import (
    Application,
)
from telegram import Update
from dotenv import load_dotenv
from database import setup
from handlers import handlers

load_dotenv()

def main():
    app = Application.builder().token(os.environ["TELEGRAM_TOKE"]).arbitrary_callback_data(True).build()
        
    for handler in handlers:
        app.add_handler(handler)

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    setup()
    main()
