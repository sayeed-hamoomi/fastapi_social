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


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="ss123123s",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("database connection was successfull")
        break
    except Exception as error:
        print("connecting to database failed")
        print("error:", error)


@app.get("/posts")
def all_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return posts
    # return Response(
    #     {"message": "successful ", "posts": posts}, status_code=status.HTTP_200_OK
    # )


@app.post("/posts")
def create_post(post: Post):
    cursor.execute(
        """ INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *  """,
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return new_post


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(
        f""" SELECT * FROM posts WHERE id={id}  """,
    )
    post = cursor.fetchone()
    return post


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """ UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING * """,
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    return updated_post


@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    return {
        "messege": "this post was deleted successfully",
        "deleted_post": deleted_post,
    }
