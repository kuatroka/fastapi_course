from fastapi import FastAPI
from . import models
from .database import Base, engine
from app import database
from .routers import post, user, auth
from .config import settings

models.Base.metadata.create_all(bind=engine)

print(settings.secret_key)
 
app = FastAPI() 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello Sergio"}



