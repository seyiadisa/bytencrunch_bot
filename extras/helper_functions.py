#random functions to help abstract messy processes
import openpyxl, os
import requests
from dotenv.main import load_dotenv
from datetime import datetime as dt
from database.queries import (
    get_todays_orders,
    get_items_from_order,
    get_product,
    get_user
)
from database.models import Order
from .my_lists import HALL_LIST


load_dotenv()

def make_excel_file(data, hall):
    wb= openpyxl.Workbook()
    worksheet =  wb.active

    for row in data:
        worksheet.append(row)

    for col in worksheet.columns:
        max_length = 0
        column = col[0].column_letter # Get the column name
        for cell in col:
            try: # Necessary to avoid error on empty cells
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        worksheet.column_dimensions[column].width = adjusted_width
    
    today_date = dt.now().date().isoformat().replace("-","_")
    wb.save(f"{hall}_{today_date}.xlsx")
    return f"{hall}_{today_date}.xlsx"
    

def sort_excel_data(send_func, update, context):
    orders = get_todays_orders()
    headers = (
        "order_id",
        "customer_name",
        "ammount_paid",
        "status",
        "hall",
        "room",
        "order_details"
    )
    HALL_DIC = {}
    for i in HALL_LIST:
        HALL_DIC[i] = (headers,)

    for order in orders:
        order_data = order.get_data_as_tuple()
        HALL_DIC[order.hall] += order_data

    for hall, data in HALL_DIC.items():
        file_name = make_excel_file(data, hall)
        send_func(update, context,file_name)

def order_dict(order:Order):
    order_items = get_items_from_order(order)

    order_details = ""
    for item in order_items:
        product = get_product(item.product_id)
        order_details += f"{item.item_count} order(s) of {product.name} \n"

    result = (
        order.my_id,
        order.customer_name,
        order.ammount_paid,
        order.status,
        order.hall,
        order.room,
        order_details,
    )
    return result
    
def get_user_profile(user_id):
    user_data = get_user(user_id)
    text_to_return = f"""
                    User Profile
                    Name => {user_data[1]}
                    /update_user_name
                    Matric_Number => {user_data[2]}
                    **You can't change your matric number**
                    Email => {user_data[3]}
                    **You can't change your matric number or email**
                    Hall => {user_data[4]}
                    /update_user_hall
                    Room => {user_data[5]}
                    /update_user_room
                    """
    # """
    #                 /update_user_email
    #                 To re-enter all you details,
    #                 /update_user_all_details
    #                 """
    return text_to_return

def get_flutterwave_link(reference, amount,email):
    redirect_url = "maca.com"
    flutterwave_url = 'https://api.flutterwave.com/v3/payments'
    secret_key = os.environ["FLUTTERWAVE_SECRET_KEY"]
    headers = {
        'Authorization': f'Bearer {secret_key}',
        'Content-Type': 'application/json',
    }
    data = {
        'tx_ref' : reference,
        'amount' : amount,
        'redirect_url' : redirect_url,
        'customer' : {
            'email': email,
        },
        'customization' : {
            'title': "BytenCrunch",
        },
    }
    
    response = requests.post(flutterwave_url, headers=headers, json=data)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    flutterwave_response = response.json()

    if flutterwave_response.get('status', False):
        payment_url = flutterwave_response['data']['link']
        return payment_url
    else:
        print("Failed to get payment url")
        return {"status": "failed", "error": "Payment initialization failed"}
