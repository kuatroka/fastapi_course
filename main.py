from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
           {"title": "favourite food", "content": "I like pizza", "id": 2}]


@app.get("/")
def root():
    return {"message": "Hello Sergio"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}
    # return {"new_post": f"title: {payload['title']} content: {payload['content']} "}


# title str, content str


@app.get("/plonker")
def plonker():
    return {"message": "Rodney...you're such a plonker!!"}