from telegram.ext import (
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    filters
)
from extras.keyboards import PAYMENT_OPTION_KEYBOARD, form_keyboard
from extras.helper_functions import get_flutterwave_link
import uuid

#presents the user with payment options to choose from
async def payment_option(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    reference = str(uuid.uuid4())
    # query_data = update.callback_query.data
    link = get_flutterwave_link()
    
    
    
    await context.bot.send_message(
        chat_id = chat_id,
        text=f"Click the link below to make payment \n {link} \n\n Have you made payments?",
        reply_markup = form_keyboard(PAYMENT_OPTION_KEYBOARD)
    )
    
    
    

payment_flow_handler = CommandHandler("payment_option", payment_option)