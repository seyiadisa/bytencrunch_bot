from .create import *

def setup():
    create_database()

    for key, val in tables.items():
        create_table(key, val)