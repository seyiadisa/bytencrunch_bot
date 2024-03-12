from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes
)
from database.queries import (
    is_user,
)
from database.models import User

from extras.keyboards import HOME_KEYBOARD

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    if is_user(update.effective_user.id):
        await home(update, context)
    else:
        user = User()
        user.userid = update.effective_user.id
        context.user_data["user"] = user
        options = ["Create Account"]
        message = await update.message.reply_text(
            text="Welcome to ByteNCrunch",
            reply_markup=build_keyboard(options)
        )   
        context.user_data["prev_message"] = message.message_id

def build_keyboard(current_list) -> InlineKeyboardMarkup:
    """Helper function to build the next inline keyboard."""
    return InlineKeyboardMarkup.from_column(
        [InlineKeyboardButton(i, callback_data=i.lower().replace(" ","")) for i in current_list]
    )

async def home(update, context):
    chat_id = update.effective_chat.id


    markup = InlineKeyboardMarkup(HOME_KEYBOARD)
    await context.bot.send_message(
        chat_id=chat_id,
        text="Welcome to ByteNCrunch",
        reply_markup = markup
    ) 

start_handler = CommandHandler("start",start)
