from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from database.connection import get_conncetion
import bcrypt

router = APIRouter()
class User(BaseModel):
    name: str
    email: str
    password: str

@router.post("/register")
def register(user: User):
    conn=get_conncetion()
    cursor=conn.cursor()
    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)", (user.name,user.email,hashed_pw))
        conn.commit()
        return {"massage": "Account created successfully"}
    except:
        raise HTTPException(status_code=400,detail="Email already exists")
