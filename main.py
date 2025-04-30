from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import routes
from app.database import SessionLocal, engine
from app import models, schemas

# Создание всех таблиц в базе данных
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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