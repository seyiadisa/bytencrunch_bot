from telegram import ForceReply, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv
import os

load_dotenv()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text("Hello! I'm a bot!")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)


def main():
    application = ApplicationBuilder().token(os.environ.get("TELEGRAM_TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("help", start))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
