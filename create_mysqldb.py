"""""
    install Mysql on your computer
    https://dev.mysql.com/downloads/installer/
    pip install pymysql
    pip install cryptography
    pip install mysql-connector-python
"""""


import mysql.connector

from decouple import config


DB = mysql.connector.connect(
    # host='url',
    # user='your_username',
    # passwd='your_password'
)

# prepare a cursor
cursor_obj = DB.cursor()

# create a DB
DB_NAME = config('DB_NAME')
cursor_obj.execute(f"CREATE DATABASE {DB_NAME}")

print("All Done!")