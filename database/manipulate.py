import mysql.connector as connector
from dotenv.main import load_dotenv
# from .models import User
import os
# from .queries import get_last_order

load_dotenv()

def update_user_data(user_id, column, data):
    mycon = connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DATABASE"],
    # port=os.environ["DB_PORT"],
    # ssl_disabled=True
    )

    crsr = mycon.cursor()
    crsr.execute(
        "UPDATE user SET {} = %s WHERE userid =%s".format(column),
        (data, user_id)
    )
    mycon.commit()

    mycon.close()