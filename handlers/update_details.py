from time import sleep
from telegram.ext import (
    CallbackQueryHandler, 
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    filters
)
from .account_creation import home
from database.manipulate import update_user_data
from extras.keyboards import (
    form_keyboard,
    HOME_KEYBOARD,
    HALL_KEYBOARD,
    CANCEL_KEYBOARD,
    CONFIRM_USER_INPUT_KEYBOARD
)
from extras.helper_functions import get_user_profile
from extras.my_lists import UPDATE_COMMAND_LIST
HALL,OTHERS,DONE, RE_ENTER=range(1,5)

async def update_details_init(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    profile = get_user_profile(user_id)
    message = await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id = context.user_data["prev_message"],
        text = profile,
        reply_markup = form_keyboard(CANCEL_KEYBOARD)
    )
    context.user_data["prev_message"] = message.message_id
    return ConversationHandler.END

async def update_details(update, context):
    chat_id = update.effective_chat.id

    await context.bot.delete_message(
        chat_id=chat_id,
        message_id=update.message.message_id
    )

    try:
        query_data = update.message.text[13:]
        context.user_data["update"] = query_data 
    except:
        pass

    query_data = context.user_data["update"]
    match query_data:
        case "all_details":
            pass
        case "hall":
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id = context.user_data["prev_message"],
                text="What hall are you in?\n(You can always change this later)",
                reply_markup=form_keyboard(HALL_KEYBOARD)
            )
            return HALL
        case _:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id = context.user_data["prev_message"],
                text=f"Enter new {query_data}:",
                reply_markup = form_keyboard(CANCEL_KEYBOARD)
            )
            return OTHERS


async def process_selection(update, context):
    chat_id = update.effective_chat.id
    selection = context.user_data["update"]

    match selection:
        case "hall":
            user_input = update.callback_query.data
        case "all_details":
            pass
        case _:
            user_input = update.message.text
            await context.bot.delete_message(
                chat_id=chat_id,
                message_id=update.message.message_id
            )

    
    context.user_data["new_data"] = user_input

    await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id = context.user_data["prev_message"],
            text=f"Your new {selection} is => '{user_input}'",
            reply_markup = form_keyboard(CONFIRM_USER_INPUT_KEYBOARD)
    )

    return DONE

# def to_the_start(update, context):


async def save_changes(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    query_data = update.callback_query.data

    match query_data:
        case "save":
            user_input = context.user_data["new_data"] 
            selection = context.user_data["update"]

            update_user_data(user_id,selection, user_input)

            for i in range(0,4):
                await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id = context.user_data["prev_message"],
                        text=f"Your changes have been saved! \n Redirecting in...{3-i}",
                        reply_markup = form_keyboard(CONFIRM_USER_INPUT_KEYBOARD)
                )
                sleep(1)
            
            await home(update, context)
        case "reenter_details":
            for i in range(0,4):
                await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id = context.user_data["prev_message"],
                        text=f"Redirecting in...{3-i}",
                        reply_markup = form_keyboard(CONFIRM_USER_INPUT_KEYBOARD)
                )
                sleep(1)

            await update_details(update, context)





view_details_handler = CallbackQueryHandler(update_details_init, "view_account_details")
update_details_handler = ConversationHandler(
    entry_points=[CommandHandler(UPDATE_COMMAND_LIST,update_details)],
    states={
        HALL:[CallbackQueryHandler(process_selection)],
        OTHERS:[MessageHandler(filters.TEXT & ~filters.COMMAND, process_selection)],
        DONE: [CallbackQueryHandler(save_changes)],
        # RE_ENTER:[CallbackQueryHandler]
    },
    fallbacks=[]
)