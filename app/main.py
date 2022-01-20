from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import Base, engine
from app import database
from .routers import post, user, auth, vote
from .config import settings
import subprocess

# models.Base.metadata.create_all(bind=engine) # not needed if using alembic for tables creation
# and modifications

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

### !!! Careful with this, it will use alembic to create tables in the DB !!! ###
### !!! I'm not sure if it's a good idea to use it this way, but I don't know how to do it in  !!! ###
### !!! docker-composer                                          !!! ###
subprocess.run(["alembic", "upgrade", "head"])


@app.get("/")
def root():
    return {"message": "hello world3!"}
