from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

CANCEL_KEYBOARD =[
    [InlineKeyboardButton(text="Cancel", callback_data="cancel")]
]

HOME_KEYBOARD =  [
    [InlineKeyboardButton(text="What's in Cafe?", callback_data="launch_mini_app"),],
    [InlineKeyboardButton(text="View Account Details", callback_data="view_account_details"),],
    [InlineKeyboardButton(text="View Order History", callback_data="view_order_history"),],
]

HALL_KEYBOARD = [
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
    ],
    # CANCEL_KEYBOARD
]

CONFIRM_USER_INPUT_KEYBOARD = [
    [InlineKeyboardButton(text="Save", callback_data="save"),],
    [InlineKeyboardButton(text="Re-enter Details", callback_data="reenter_details"),],
    # CANCEL_KEYBOARD
]

UPDATE_USER_PROFILE_KEYBOARD = [
    [InlineKeyboardButton(text="Save", callback_data="save"),],
    CANCEL_KEYBOARD
]

#Payment Keyboard
PAYMENT_OPTION_KEYBOARD = [
    [InlineKeyboardButton(text="Yes", callback_data="yes")],
    [InlineKeyboardButton(text="No", callback_data="no")]
]

#ADMIN KEYBOARD
ADMIN_START_KEYBOARD = [
    [InlineKeyboardButton(text="Get Today's Orders", callback_data="fetch_orders")]
]


def form_keyboard(kybd_btn):
    return InlineKeyboardMarkup(kybd_btn)
