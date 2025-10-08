from fastapi import FastAPI
from routers import register, login
from fastapi.middleware.cors import CORSMiddleware
from database.connection import conn
import psycopg2.extras

app = FastAPI()

app.include_router(register.router)
app.include_router(login.router)

@app.get("/")
def root():
    return {"message": "welcome to my api"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://silver9wolf.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test-db")
def test_db():
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        cursor.close()
        return {"status": "connected", "users": result}
    except Exception as e:
        return {"status": "error", "details": str(e)}