#random functions to help abstract messy processes
import openpyxl
from datetime import datetime as dt
from database.queries import (
    get_todays_orders,
    get_items_from_order,
    get_product
)
from database.models import Order
from database.queries import get_user

def make_excel_file(data):
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
    wb.save(f"{today_date}.xlsx")
    

def sort_excel_data():
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
    order_data = (headers,)
    for order in orders:
        order_data += order_dict(order) 

    return order_data

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
                    /update_user_email
                    Hall => {user_data[4]}
                    /update_user_hall
                    Room => {user_data[5]}
                    /update_user_room
                    """
    # """
    #                 To re-enter all you details,
    #                 /update_user_all_details
    #                 """
    return text_to_return


