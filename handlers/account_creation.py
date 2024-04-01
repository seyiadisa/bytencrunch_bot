from telegram.ext import (
    CallbackQueryHandler, 
    ConversationHandler,
    MessageHandler,
    filters
)


from extras.user_validators import (
    check_matno,
    check_room,
    check_email
)

from extras.keyboards import (
    form_keyboard,
    HOME_KEYBOARD,
    HALL_KEYBOARD,
    CANCEL_KEYBOARD,
    CONFIRM_USER_INPUT_KEYBOARD
)

BEGIN,NAME,MATNO,EMAIL,HOSTEL,ROOM, CONFIRM = range(0,7)

async def create_account(update, context):
    chat_id = update.effective_chat.id
    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id = context.user_data["prev_message"],
        text="Let's start setting up your account!\nWhat's your name?\n**This is what our dispatchers will yell when searching for you😗**",
        reply_markup = form_keyboard(CANCEL_KEYBOARD)
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
        reply_markup = form_keyboard(CANCEL_KEYBOARD)
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
                text="Now we need you email!\nPlease make sure to use your Covenant University email!",
                reply_markup = form_keyboard(CANCEL_KEYBOARD)
                
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
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id = context.user_data["prev_message"],
                text="What hall are you in?\n(You can always change this later)",
                reply_markup=form_keyboard(HALL_KEYBOARD)
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
        text="Lastly we need your room number",
        reply_mark=form_keyboard(CANCEL_KEYBOARD)
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

            
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id = context.user_data["prev_message"],
                text=text_to_send,
                reply_markup = form_keyboard(CONFIRM_USER_INPUT_KEYBOARD)
            )

            return CONFIRM
        case False:
            await redo_room(update,context, user.room)

async def finalise(update, context):
    query = update.callback_query
    data = query.data
    match data:
        case "save":
            user = context.user_data["user"]
            user.save()
            await home(update, context)

        case "reenter_details":
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
                text=text,
                reply_markup = form_keyboard(CANCEL_KEYBOARD)
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
                text=text,
                reply_markup = form_keyboard(CANCEL_KEYBOARD)
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
                text=text,
                reply_markup = form_keyboard(CANCEL_KEYBOARD)
            )
    return ROOM

#Welcome message after saving!
async def home(update, context):
    chat_id = update.effective_chat.id

    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id = context.user_data["prev_message"],
        text="Welcome to ByteNCrunch",
        reply_markup = form_keyboard(HOME_KEYBOARD)
    )
    return -1


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
