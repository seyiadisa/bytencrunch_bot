import os
from datetime import datetime as dt
import mysql.connector as connector
from dotenv import load_dotenv
from .models import Order

load_dotenv()


#user queries
def is_user(userid = None) -> bool:
    '''Check if id is that of a user'''
    mydb = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DATABASE"]
    )

    crsr = mydb.cursor()
    crsr.execute(
        "SELECT * FROM user WHERE userid=%s",
        (userid,)
    )
    result = crsr.fetchall()
    mydb.close()
    if result == []:
        return False
    else:
        return True
    
def get_user(userid):
    mydb = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DATABASE"]
    )

    crsr = mydb.cursor()
    crsr.execute(
        "SELECT * FROM user WHERE userid=%s",
        (userid,)
    )
    result = crsr.fetchall()[0]
    mydb.close()
    return result

def get_user_room(userid):
    mydb = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DATABASE"]
    )
    crsr = mydb.cursor()
    crsr.execute(
        "SELECT * FROM user WHERE userid=%s",
        (userid,)
    )

    result = crsr.fetchall()[0][4]
    mydb.close()
    return result

def get_user_name(userid):
    mydb = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DATABASE"]
    )
    crsr = mydb.cursor()
    crsr.execute(
        "SELECT * FROM user WHERE userid=%s",
        (userid,)
    )

    result = crsr.fetchall()[0][1]
    mydb.close()
    return result

#vendor queries
def get_all_vendors():
    mydb = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DATABASE"]
    )
    crsr = mydb.cursor()
    crsr.execute(
        "SELECT * FROM vendor"
    )
    result = crsr.fetchall()
    mydb.close()
    return result


#product queries
def get_product(product_id):
    mydb = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DATABASE"]
    )
    crsr = mydb.cursor()
    crsr.execute(
        "SELECT * FROM product WHERE id=%s",
        (product_id,)
    )

    result = crsr.fetchall()[0]
    mydb.close()

    return result

def get_all_products() -> list:
    mydb = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DATABASE"]
    )
    crsr = mydb.cursor()
    crsr.execute(
        "SELECT * FROM product"
    )

    result = crsr.fetchall()

    mydb.close()

    return result
   

def get_products_from(myid):
    mydb = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DATABASE"]
    )
    crsr = mydb.cursor()
    crsr.execute(
        "SELECT * FROM product WHERE vendorID=%s",(myid,)
    )

    result = crsr.fetchall()
    mydb.close()
    return result



#Order Queries
def get_all_orders():
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"]
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM orders"
    )

    result = crsr.fetchall()
    mycon.close()
    return result


def get_todays_orders():
    today = dt.now().date()
    all_orders = get_all_orders()
    today_orders = []
    for my_order in all_orders:
        if my_order[-1].date() == today:
            today_orders.append(Order(my_order))

    return today_orders


#OrderItems Queries
def get_all_order_items():
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"]
    )
    crsr = mycon.cursor()
    crsr.execute(
        "SELECT * FROM order_item"
    )

    result = crsr.fetchall()
    mycon.close()
    return result