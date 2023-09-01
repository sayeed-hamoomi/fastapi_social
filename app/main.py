from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, get_db
from app.routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

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
