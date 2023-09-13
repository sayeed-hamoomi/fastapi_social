from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.oauth2 import get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=schemas.CommentResponce)
def add_comment(
    comment: schemas.Comment,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_comment = models.Comment(**comment.dict(), user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/{post_id}", response_model=List[schemas.CommentResponce])
def all_comments(
    post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()
    return comments
