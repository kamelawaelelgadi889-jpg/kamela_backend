from fastapi import FastAPI
from routers import register ,login
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.include_router(register.router)
app.include_router(login.router)
app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
)