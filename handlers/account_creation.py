from telegram.ext import (
    CallbackQueryHandler, 
    ConversationHandler,
    MessageHandler,
    filters
)
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

NAME,MATNO,EMAIL,HOSTEL,ROOM = range(0,5)

def create_account(update, context):
    query = update.callback_query
    chat_id = update.effective_chat.id
    message = context.bot.edit_message_text(
        chat_id=chat_id,
        message_id = context.user_data["prev_message"],
        text="Let's start setting up your account!\nWhat's your name?\n***This is what our dispatchers will yell when searching for you😗***",
    )

    context.user_data["prev_message"] = message.message_id

    return NAME 

def enter_matno(update, context):
    chat_id = update.effective_chat.id

    user = context.user_data["user"]
    user.name = update.message.text

    context.bot.delete_message(
        chat_id=chat_id,
        message_id=update.message.message_id
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=context.user_data["prev_message"]
    )
    message = context.bot.send_message(
        chat_id = chat_id,
        text="Okay, next up is your matric number\n~Please be good and enter it correctly~",
    )

    context.user_data["user"] = user
    context.user_data["prev_message"] = message.message_id

    return MATNO

async def enter_email(update, context):
    chat_id = update.effective_chat.id

    user = context.user_data["user"]
    user.matno = update.message.text

    context.bot.delete_message(
        chat_id=chat_id,
        message_id=update.message.message_id
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=context.user_data["prev_message"]
    )
    message = context.bot.send_message(
        chat_id = chat_id,
        text="Now we need you email!"
    )

    context.user_data["user"] = user
    context.user_data["prev_message"] = message.message_id

    return EMAIL

def select_hostel(update, context):
    chat_id = update.effective_chat.id

    user = context.user_data["user"]
    user.email = update.message.text

    context.bot.delete_message(
        chat_id=chat_id,
        message_id=update.message.message_id
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=context.user_data["prev_message"]
    )
    reply_keyboard = [
        [
            InlineKeyboardButton(text="Peter Hall", callback_data="Peter Hall"),
            InlineKeyboardButton(text="Paul Hall", callback_data="Paul Hall"),
            InlineKeyboardButton(text="John Hall", callback_data="John Hall"),
            InlineKeyboardButton(text="Joseph Hall", callback_data="Joseph Hall"),
            InlineKeyboardButton(text="Daniel Hall", callback_data="Daniel Hall"),

        ],
        [
            InlineKeyboardButton(text="Esther Hall", callback_data="Esther Hall"),
            InlineKeyboardButton(text="Mary Hall", callback_data="Mary Hall"),
            InlineKeyboardButton(text="Deborah Hall", callback_data="Deborah Hall"),
            InlineKeyboardButton(text="Dorcas Hall", callback_data="Dorcas Hall"),
            InlineKeyboardButton(text="Lydia Hall", callback_data="Lydia Hall"),

        ]

    ]
    markup = InlineKeyboardMarkup(reply_keyboard)
    context.bot.send_message(
        chat_id = chat_id,
        text="What hostel are you in?\n(You can always change this later)",
        reply_keyboard=markup
    )
    
    context.user_data["user"] = user

    return HOSTEL

def enter_room(update, context):
    query = update.callback_query
    chat_id = update.effective_chat.id

    user = context.user_data["user"]
    user.hostel = query.data

    context.bot.delete_message(
        chat_id=chat_id,
        message_id=update.message.message_id
    )
    message = query.edit_message_text(
        chat_id = chat_id,
        text="Lastly we need your room number and hostel"
    )
    
    context.user_data["user"] = user
    context.user_data["prev_message"] = message.message_id

    return ROOM


create_account_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(create_account, "createaccount")],
    states={
        NAME : [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_matno)],
        MATNO : [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_email)],
        EMAIL : [MessageHandler(filters.TEXT & ~filters.COMMAND, select_hostel)],
        HOSTEL : [CallbackQueryHandler(enter_room)]        
    },
    fallbacks=[]
)