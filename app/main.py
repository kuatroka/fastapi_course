from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    # print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id: {id} not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} does not exist")
    conn.commit()
    return {'message': f'post with id: {id} was succesfully deleted'}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} does not exist")

    return {"data": f"Post with id: {id} has been succesfully updated as {updated_post}"}




@app.get("/plonker")
def plonker():
    return {"message": "Rodney...you're such a plonker!!"}