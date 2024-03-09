import os
from dotenv import load_dotenv
import mysql.connector as connector

load_dotenv()


class User:
    userid = None
    name = None
    matno = None
    email =  None
    hostel=None
    room = None
    

    def save(self):
        mydb = connector.connect(
            host=os.environ["DB_HOST"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DATABASE"]
        )
        crsr = mydb.cursor()
        crsr.execute(
            "INSERT into user (userid, name, matno, email, hostel, room , account_number,bank) VALUES (%s,%s,%s,%s,%s,%s)",
            (self.userid, self.name, self.matno, self.email,self.hostel, self.room)
                     )
        mydb.commit()
        mydb.close()

    def __str__(self) -> str:
        return f"User(userid={self.userid}, name={self.name}, matno={self.matno}, email={self.email}, hostel={self.hostel}, room={self.room})"
    



class Vendor:
    userid = None
    name = None
    bank = None
    account_number = None

    def __str__(self) -> str:
        return f"Vendor(userid={self.userid}, name={self.name}, bank={self.bank}, account_number={self.account_number})"
    


class Product:
    my_id = None
    name = None
    vendorID = None
    price = None
    type = None
    sides = None

    def __str__(self) -> str:
        return f"Product(id={self.my_id}, name={self.name}, vendorID = {self.vendorID}, price={self.price}, type={self.type}, sides={self.sides})"
    



class Order:
    my_id = None
    customer_id = None
    customer_name = None
    ammount_paid = None
    payment_status = None
    status = "pending"
    def __init__(self, my_dic: dict) -> None:
        self.my_id, self.customer_id, self.ammount_paid, self.payment_status, self.status = my_dic.values()
    def __str__(self) -> str:
        return f"Order(id={self.my_id}, customer_id ={self.customer_id}, customer_name={self.customer_name}, ammount_paid={self.ammount_paid}, payment_status={self.payment_status}, status={self.status})"
    
    


class OrderItem:
    my_id = None
    product_id=None
    order_id = None
    item_count = None
    subtotal = None

    def __str__(self) -> str:
        return f"OrderItem(id={self.my_id}, product_id={self.product_id}, order_id={self.order_id}, item_count={self.item_count}, subtotal={self.subtotal})"
    

