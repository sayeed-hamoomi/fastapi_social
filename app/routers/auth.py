from fastapi import APIRouter, Depends, HTTPException, status
from app import schemas, models, utils, oauth2
from sqlalchemy.orm import Session
from app.database import get_db


router = APIRouter()


@router.post("/login")
def login(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    u = db.query(models.User).filter(models.User.email.ilike(user_login.email)).first()
    if not u:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"INVALID CREDENTIALS"
        )
    if not utils.verify_pwd(user_login.password, u.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"INVALID CREDENTIALS"
        )
    access_token = oauth2.create_access_token({"user_id": u.id})

    return {"access_token": access_token, "token_type": "bearer"}
