import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME  # import from config.py


# ========================== #
# DATABASE CONNECTION METHOD #
# ========================== #
def connect_to_db():
    """This simple method is essential to connect to the main db. It uses a .env file
    that you need to create yourself with your credentials, named exactly as follows:
    - host = DB_HOST,
    - user = DB_USER,
    - password = DB_PASSWORD,
    - database = DB_NAME <- this will probably disappear in following commits as it will
    be the same for everyone
    """
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    return conn
