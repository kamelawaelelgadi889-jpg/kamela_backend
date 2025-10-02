from database.connection import get_conncetion

conn=get_conncetion()
cursor=conn.cursor()
cursor.execute("SHOW TABLES")
tables=cursor.fetchall()
print("tabeles in database:",tables)