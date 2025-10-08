from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import conn
import bcrypt
import psycopg2.extras

router = APIRouter()

class User(BaseModel):
    name: str
    email: str
    password: str

@router.post("/register")
def register(user: User):
    cursor = conn.cursor()
    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (user.name, user.email, hashed_pw)
        )
        conn.commit()
        cursor.close()
        return {"message": "Account created successfully"}
    except Exception as e:
        cursor.close()
        raise HTTPException(status_code=400, detail="Email already exists")