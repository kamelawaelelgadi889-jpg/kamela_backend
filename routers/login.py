from fastapi import APIRouter, HTTPException, status

from pydantic import BaseModel
import bcrypt
from database.connection import get_conncetion
#تعريف الراوتر 
router =APIRouter()
#تعريف البياتات اللي المستخدم يرسلها
class LoginInput(BaseModel):
    email: str
    password:str

#تعريف مسار تسجيل الدخول 
@router.post("/login")
def login(data: LoginInput ):
    conn = get_conncetion()
    cursor = conn . cursor(dictionary= True)
    #البحت عن المستخدم حسب الايميل
    cursor.execute("SELECT * FROM users WHERE email = %s", (data.email,))
    user = cursor.fetchone()
    #التاكد من كلمة المرور 
    if user and bcrypt.checkpw(data.password.encode("utf-8"), user["password"].encode("utf-8")):
        return {"massage": "Lodin successful",
                "user": {"name":user["name"],
                         "id":user["id"],
                         "email":user["email"]}}
    else:
        raise HTTPException(status_code=400, detail="Invalid email or password")