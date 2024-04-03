from .start import start_handler
from .account_creation import create_account_handler
from .update_details import view_details_handler,update_details_handler
from .payment_method import payment_flow_handler
handlers = [
    start_handler,
    create_account_handler, 
    view_details_handler,
    update_details_handler,
    payment_flow_handler
]
