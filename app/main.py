from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from app import models
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

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
def all_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts
    # return Response(
    #     {"message": "successful ", "posts": posts}, status_code=status.HTTP_200_OK
    # )


@app.post("/posts")
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # cursor.execute(
    #     """ INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *  """,
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    return new_post


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # cursor.execute(
    #     f""" SELECT * FROM posts WHERE id={id}  """,
    # )
    # post = cursor.fetchone()
    return post


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # post=post_query.first()
    updated_post = post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    # cursor.execute(
    #     """ UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING * """,
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    return post_query.first()


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted = post_query.delete(synchronize_session=False)
    db.commit()

    # cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    return {
        "messege": "this post was deleted successfully",
    }
