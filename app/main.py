from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# database stuff
from sqlalchemy.orm import Session
from app import schemas
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)


app = FastAPI() 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi_db',
                                user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('DB connection established')
        break
    except Exception as error:
        print('Connecting to DB failed')
        print('Error: ', error)
        # time.sleep(3)

@app.get("/")
def root():
    return {"message": "Hello Sergio"}



