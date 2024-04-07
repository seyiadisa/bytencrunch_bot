import os
from telegram.ext import (
    CommandHandler,
)
from extras.keyboards import ADMIN_START_KEYBOARD, form_keyboard
from extras.helper_functions import sort_excel_data

async def start(update, context):
    chat_id = update.effective_chat.id
    message = await context.bot.send_message(
        chat_id=chat_id,
        text="Hi, what would you want to do today?",
        reply_markup = form_keyboard(ADMIN_START_KEYBOARD)
    ) 
    context.user_data["prev_message"] = message.message_id


async def get_today_orders(update, context):
    chat_id = update.effective_chat.id
    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id = context.user_data["prev_message"],
        text="Here are today's orders!",
    )
    await sort_excel_data(send_file, update, context)

def send_file(update, context, filename):
    context.bot.send_document(update.effective_chat.id, open(filename, 'rb'))
    os.remove(filename)

admin_start_handler = CommandHandler("start", get_today_orders)
