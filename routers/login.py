from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import bcrypt
import psycopg2.extras
from database.connection import conn
#تعريف الراوتر 
router =APIRouter()
#تعريف البياتات اللي المستخدم يرسلها
class LoginInput(BaseModel):
    email: str
    password:str

#تعريف مسار تسجيل الدخول 
@router.post("/login")
def login(data: LoginInput ):

    import psycopg2.extras
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    #البحت عن المستخدم حسب الايميل
    cursor.execute("SELECT * FROM users WHERE email = %s", (data.email,))
    user = cursor.fetchone()
    cursor.close()
    #التاكد من كلمة المرور 
    if user and bcrypt.checkpw(data.password.encode("utf-8"), user["password"].encode("utf-8")):
        return {"message": "Login successful",
                "user": {"name":user["name"],
                         "id":user["id"],
                         "email":user["email"]}}
    else:
        raise HTTPException(status_code=400, detail="Invalid email or password")