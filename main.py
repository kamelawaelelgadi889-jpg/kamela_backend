from fastapi import FastAPI
from routers import register ,login

app = FastAPI()
app.include_router(register.router)
app.include_router(login.router)
