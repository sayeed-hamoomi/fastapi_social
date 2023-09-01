from typing import List
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session


from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/posts")


@router.get("/", response_model=List[schemas.Post])
def all_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts
    # return Response(
    #     {"message": "successful ", "posts": posts}, status_code=status.HTTP_200_OK
    # )


@router.post("/", response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db)):
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


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # cursor.execute(
    #     f""" SELECT * FROM posts WHERE id={id}  """,
    # )
    # post = cursor.fetchone()
    return post


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db)):
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


@router.delete("/{id}")
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
