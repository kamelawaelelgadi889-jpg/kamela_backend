import mysql.connector

def get_conncetion():
    return mysql.connector.connect(
        host="sql210.infinityfree.com",
        user="if0_40098443",
        password="PCXvUKJsHvXADK",
        database="users",
    )