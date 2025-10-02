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