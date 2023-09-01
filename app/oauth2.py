from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "SUYFGD84685454dhygsiugixjkd56dsjhbiklkihsd757"
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token
