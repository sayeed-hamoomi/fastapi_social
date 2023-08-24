from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()
posts = []


def find_post(id):
    for i in posts:
        if i["id"] == id:
            print("e")
            return i


class Post(BaseModel):
    title: str
    content: str


@app.get("/")
async def root():
    return {"message": "Hello sayeed"}


@app.get("/posts")
def all_posts():
    return posts


@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    return find_post(id)


@app.post("/create")
def sayeedspost(body: Post):
    body = body.dict()
    body["id"] = randrange(1, 1000000)

    posts.append(body)
    return body
