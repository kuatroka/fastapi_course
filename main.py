from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()




@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": "this is your post"}

@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message": "succesfully created posts"}


@app.get("/plonker")
def plonker():
    return {"message": "Rodney...you're such a plonker!!"}