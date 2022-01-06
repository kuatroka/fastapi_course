from typing import Optional
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
from . import models, schemas

from .database import engine, get_db

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
         


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
           {"title": "favourite food", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def root():
    return {"message": "Hello Sergio"}


@app.get("/posts")

        # Bring data from DB using SQL 
# def get_posts():
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
        # Bring data from DB using SQLAlchemy ORM
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
        # Create post with SQL
# def create_posts(post: Post):
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
#                     (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data": new_post}

        # Create post with SQLAlchemy
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # print(**post.dict())
    new_post = models.Post(**post.dict()) # needed not to type manually all the fields in the model

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


@app.get("/posts/{id}")
        # Using SQL
# def get_post(id: int):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
#     post = cursor.fetchone()

        # Using SQLAlchemy
def get_post(id: int, db: Session = Depends(get_db)):    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post) 
 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id: {id} not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)

        # Using SQL
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
#     deleted_post = cursor.fetchone()

        # Using SQLAlchemy
def delete_post(id: int, db: Session = Depends(get_db)): 
    deleted_post = db.query(models.Post).filter(models.Post.id == id)      

    if not deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} does not exist")
    # conn.commit()
    # return {'message': f'post with id: {id} was succesfully deleted'}

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return  {'message': f'post with id: {id} was succesfully deleted'}


@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #                 (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id) 


    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} does not exist")

    updated_post.update(post.dict(), synchronize_session=False)
    
    db.commit()
    # return {"data": updated_post.first()}
    return {"data": f"Post with id: {id} has been succesfully updated as"}, updated_post.first()

