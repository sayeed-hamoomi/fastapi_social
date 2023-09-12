from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security.oauth2 import OAuth2PasswordBearer
from app import models
from app.config import settings
from app.database import get_db

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_EXPIRE_MINUTES = settings.access_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token


def verify_access_token(token: str, credentials_exceptions):
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = token_data["user_id"]
        if not user_id:
            raise credentials_exceptions

    except JWTError as e:
        raise credentials_exceptions

    return user_id


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID TOKEN"
    )
    id = verify_access_token(token, credentials_exceptions=credentials_exceptions)
    if not id:
        raise credentials_exceptions
    user = db.query(models.User).filter(models.User.id == id).first()
    return user
