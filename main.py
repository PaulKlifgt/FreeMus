from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import routes
from app.database import SessionLocal, engine
from app import models, schemas

# Создание всех таблиц в базе данных
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:80",
    "http://127.0.0.1:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# регистрация
@app.post('/users/register/')
def register(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return routes.register(user=user, db=db)

#авторизация
@app.post('/users/login/')
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return routes.login(user=user, db=db)
    

#пример ручки для получения данных по токену
@app.post('/users/me/')
def read_me(token: schemas.TokenGet, db: Session = Depends(get_db)):
    return routes.read_me(token=token, db=db)