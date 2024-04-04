from telegram.ext import (
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    filters
)
from extras.keyboards import PAYMENT_OPTION_KEYBOARD, form_keyboard

#presents the user with payment options to choose from
async def payment_option(update, context):
    chat_id = update.effective_chat.id
    # user_id = update.effective_user.id
    # query_data = update.callback_query.data
    
    
    await context.bot.send_message(
        chat_id = chat_id,
        text="How would you like to make payments?",
        reply_markup = form_keyboard(PAYMENT_OPTION_KEYBOARD)
    )
    
    
    

payment_flow_handler = CommandHandler("payment_option", payment_option)