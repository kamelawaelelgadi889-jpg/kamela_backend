import os
import psycopg2

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"), 
    dbname=os.getenv("DB_NAME"),
    port=os.getenv("DB_PORT"),
    sslmode="require"
)
print("DB_HOST:", repr(os.getenv("DB_HOST")))