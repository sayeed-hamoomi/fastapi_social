from typing import List
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app import utils

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/users")


@router.post("/", response_model=schemas.user_responce)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    user.password = utils.hash_pwd(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.user_responce)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user
