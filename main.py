from telegram.ext import (
    Application,
    PicklePersistence
)
from telegram import Update
from database import setup
from handlers import handlers


def main():
    persistence = PicklePersistence(filepath='BYTE_CRUNCH_NEW')
    app = Application.builder().token("6949667326:AAHhRmiYdDU3hXYPRmWpSTi2RpXHdYjKR_Y").arbitrary_callback_data(True).build()
        
    for handler in handlers:
        app.add_handler(handler)

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    setup()
    main()
