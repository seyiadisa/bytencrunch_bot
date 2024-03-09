import os
from dotenv import load_dotenv
import mysql.connector as connector

 
load_dotenv()

tables = tables = {
    "user" : """
                    userid BIGINT PRIMARY KEY, 
                    name VARCHAR(120), 
                    matno CHAR(15) UNIQUE,
                    email VARCHAR(70), 
                    hostel VARCHAR(50),
                    room VARCHAR(255),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    """,
    "vendor" : """
                    userid BIGINT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(120),
                    UNIQUE (name),
                    bank VARCHAR(240),
                    account_number CHAR(10)
                    """,
    "product" : """
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(120),
                    vendorID BIGINT,
                    price INT,
                    type VARCHAR(25),
                    sides VARCHAR(120),
                    FOREIGN KEY (vendorID) REFERENCES vendor(userid)
                    """,
    "orders" : """
                    id INT AUTO_INCREMENT PRIMARY KEY ,
                    customer_id BIGINT,
                    customer_name VARCHAR(120),
                    ammount_paid INT,
                    payment_status CHAR(25),
                    status CHAR(25) DEFAULT 'pending',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES user(userid)
                    """,
    "order_item" : """
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        product_id INT,
                        order_id INT,
                        item_count INT,
                        subtotal INT,
                        FOREIGN KEY (product_id) REFERENCES product(id),
                        FOREIGN KEY (order_id) REFERENCES orders(id)
                        """,
    "flutter_payment" :"""
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            user_id BIGINT,
                            order_item VARCHAR(300),
                            amount DECIMAL(15, 2),
                            reference VARCHAR(100),
                            status CHAR(20) DEFAULT 'pending',
                            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                            """

}


def create_database():
    mydb = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )
    crsr = mydb.cursor()
    crsr.execute("CREATE DATABASE IF NOT EXISTS {}".format(os.environ["DATABASE"]))
    mydb.commit()

def create_table( name, fields):
    mydb = connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DATABASE"]
    )

    operation = "CREATE TABLE IF NOT EXISTS {} ({})".format(name, fields)
    crsr = mydb.cursor()
    print(name)
    crsr.execute(operation)
    mydb.commit()
