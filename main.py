import os
import psycopg2
from fastapi import FastAPI
from routers import register ,login
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(register.router)
app.include_router(login.router)
@app.get("/")
def root():
    return {"message": "welcom to my api"}
app.add_middleware(
      CORSMiddleware,
      allow_origins=["https://silver9wolf.github.io"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
)
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    dbname=os.getenv("DB_NAME"),
    port=os.getenv("DB_PORT"),
    sslmode="require"
)
@app.get("/test-db")
def test_db():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        return {"status": "connected", "users": result}
    except Exception as e:
        return {"status": "error", "details": str(e)}