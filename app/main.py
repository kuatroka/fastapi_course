from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
# from passlib.context import CryptoContext
from passlib.context import CryptContext
# database stuff
from sqlalchemy.orm import Session
from app import schemas
from . import models, schemas
from .database import engine, get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)


app = FastAPI() 

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


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id: {id} not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)): 
    deleted_post = db.query(models.Post).filter(models.Post.id == id)      
    if not deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} does not exist")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return  {'message': f'post with id: {id} was succesfully deleted'}


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(models.Post.id == id) 
    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} does not exist")
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict()) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


