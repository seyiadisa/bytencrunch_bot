from telegram import (
    InlineKeyboardButton
)

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
    ]
]

CONFIRM_USER_INPUT_KEYBOARD = [
    [InlineKeyboardButton(text="Save", callback_data="save"),],
    [InlineKeyboardButton(text="Re-enter Details", callback_data="reenter_details"),]
]