import mysql.connector

def get_conncetion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="user",
    )