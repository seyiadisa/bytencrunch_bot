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


from extras.user_validators import (
    check_matno,
    check_room,
    check_email
)

BEGIN,NAME,MATNO,EMAIL,HOSTEL,ROOM, CONFIRM = range(0,7)

async def create_account(update, context):
    chat_id = update.effective_chat.id
    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id = context.user_data["prev_message"],
        text="Let's start setting up your account!\nWhat's your name?\n**This is what our dispatchers will yell when searching for you😗**",
    )

    return NAME 

async def enter_matno(update, context):
    chat_id = update.effective_chat.id

    user = context.user_data["user"]
    user.name = update.message.text

    await context.bot.delete_message(
        chat_id=chat_id,
        message_id=update.message.message_id
    )

    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id = context.user_data["prev_message"],
        text="Okay, next up is your matric number\n~Please be good and enter it correctly~",
    )

    context.user_data["user"] = user
    
    return MATNO

async def enter_email(update, context):
    chat_id = update.effective_chat.id

    user = context.user_data["user"]
    user.matno = update.message.text

    await context.bot.delete_message(
                chat_id=chat_id,
                message_id=update.message.message_id
            )
    
    match check_matno(user.matno):
        case True:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id = context.user_data["prev_message"],
                text="Now we need you email!\nPlease make sure to use your Covenant University email!"
            )

            context.user_data["user"] = user

            return EMAIL
        case False:
            await redo_mat_no(update,context, user.matno)

async def select_hostel(update, context):
    chat_id = update.effective_chat.id

    user = context.user_data["user"]
    user.email = update.message.text

    await context.bot.delete_message(
        chat_id=chat_id,
        message_id=update.message.message_id
    )

    match check_email(user.email):
        case True:
            reply_keyboard = [
                [
                    InlineKeyboardButton(text="Peter Hall", callback_data="Peter Hall"),
                    InlineKeyboardButton(text="Esther Hall", callback_data="Esther Hall"),
                ],
                [
                    InlineKeyboardButton(text="Joseph Hall", callback_data="Joseph Hall"),
                    InlineKeyboardButton(text="Lydia Hall", callback_data="Lydia Hall"),

                ],
                [
                    InlineKeyboardButton(text="Paul Hall", callback_data="Paul Hall"),
                    InlineKeyboardButton(text="Mary Hall", callback_data="Mary Hall"),
                ],
                [
                    InlineKeyboardButton(text="John Hall", callback_data="John Hall"),
                    InlineKeyboardButton(text="Deborah Hall", callback_data="Deborah Hall"),
                ],
                [
                    InlineKeyboardButton(text="Daniel Hall", callback_data="Daniel Hall"),
                    InlineKeyboardButton(text="Dorcas Hall", callback_data="Dorcas Hall"),
                ]
            ]
            markup = InlineKeyboardMarkup(reply_keyboard)
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id = context.user_data["prev_message"],
                text="What hall are you in?\n(You can always change this later)",
                reply_markup=markup
            )
            
            context.user_data["user"] = user

            return HOSTEL
        case False:
            await redo_email(update, context, user.email)

async def enter_room(update, context):
    query = update.callback_query
    chat_id = update.effective_chat.id

    user = context.user_data["user"]
    user.hall = query.data

    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id = context.user_data["prev_message"],
        text="Lastly we need your room number"
    )
    
    context.user_data["user"] = user

    return ROOM

async def confirm_details(update, context):
    chat_id = update.effective_chat.id

    user = context.user_data["user"]
    user.room = update.message.text

    await context.bot.delete_message(
                chat_id=chat_id,
                message_id=update.message.message_id
            )

    match check_room(user.room):
        case True:
            text_to_send = f'''
            Here's what you entered:
            Name:{user.name}
            MatNo:{user.matno}
            Email:{user.email}
            Hall:{user.hall}
            Room:{user.room}
            \nPlease make sure that it's all correct
            '''

            reply_keyboard = [
                [InlineKeyboardButton(text="Save", callback_data="save_user"),],
                [InlineKeyboardButton(text="Re-enter Details", callback_data="redo_user_details"),]
            ]

            markup = InlineKeyboardMarkup(reply_keyboard)
            
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id = context.user_data["prev_message"],
                text=text_to_send,
                reply_markup = markup
            )

            return CONFIRM
        case False:
            await redo_room(update,context, user.room)

async def finalise(update, context):
    query = update.callback_query
    data = query.data
    match data:
        case "save_user":
            user = context.user_data["user"]
            user.save()
            await home(update, context)

        case "redo_user_details":
            return BEGIN

#Re-enter functions after validation
async def redo_mat_no(update, context, matno):
    chat_id = update.effective_chat.id
    
    text=f'''
        Invalid matric number
        Here's what you entered:
            "{matno}"
        \nPlease enter a valid matric number!
                '''
    await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id = context.user_data["prev_message"],
                text=text
            )
    return MATNO

async def redo_email(update, context, email):
    chat_id = update.effective_chat.id
    
    text=f'''
        Invalid email, make sure you're using you school email!
        Here's what you entered:
            "{email}"
        \nPlease enter a valid school email!
                '''
    await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id = context.user_data["prev_message"],
                text=text
            )
    return EMAIL

async def redo_room(update, context, room):
    chat_id = update.effective_chat.id
    
    text=f'''
        Invalid room number
        Here's what you entered:
            "{room}"
        \nPlease enter a valid room number!
                '''
    await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id = context.user_data["prev_message"],
                text=text
            )
    return ROOM

#Welcome message after saving!
async def home(update, context):
    chat_id = update.effective_chat.id

    reply_keyboard = [
        [InlineKeyboardButton(text="What's in Cafe", callback_data="launch_mini_app"),],
        [InlineKeyboardButton(text="View Account Details", callback_data="view_account_details"),],
        [InlineKeyboardButton(text="View Order History", callback_data="view_order_history"),],
    ]

    markup = InlineKeyboardMarkup(reply_keyboard)
    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id = context.user_data["prev_message"],
        text="Welcome to ByteNCrunch",
        reply_markup = markup
    )
    return ConversationHandler.END


create_account_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(create_account, "createaccount")],
    states={
        BEGIN : [CallbackQueryHandler(create_account)],
        NAME : [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_matno)],
        MATNO : [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_email)],
        EMAIL : [MessageHandler(filters.TEXT & ~filters.COMMAND, select_hostel)],
        HOSTEL : [CallbackQueryHandler(enter_room)],
        ROOM : [MessageHandler(filters.TEXT & ~filters.COMMAND,confirm_details)],
        CONFIRM: [CallbackQueryHandler(finalise)]
    },
    fallbacks=[]
)