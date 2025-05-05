from typing import Optional
from fastapi import FastAPI, Depends, Header
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine

import auth.models, auth.routes, auth.schemas
import songs.models, songs.routes, songs.schemas
        

# Создание всех таблиц в базе данных
auth.models.Base.metadata.create_all(bind=engine)
songs.models.Base.metadata.create_all(bind=engine)


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
async def register(user: auth.schemas.UserLogin, db: Session = Depends(get_db)):
    return await auth.routes.register(user=user, db=db)

#авторизация
@app.post('/users/login/')
async def login(user: auth.schemas.UserLogin, db: Session = Depends(get_db)):
    return await auth.routes.login(user=user, db=db)
    

#пример ручки для получения данных по токену
@app.post('/users/me/')
async def read_me(token: auth.schemas.TokenGet, db: Session = Depends(get_db)):
    return await auth.routes.read_me(token=token, db=db)


@app.get('/')
async def main(db: Session = Depends(get_db)):
    data = '<!DOCTYPE html><html><head><title>FastAPI video streaming</title></head><body><audio width="1200" controls><source src="http://127.0.0.1:8000/get_song/" type="audio/mp3" /></audio></body></html>'

    return HTMLResponse(data)


@app.get('/get_song/')
async def get_song(db: Session = Depends(get_db), range: Optional[str] = Header(None)):
    return await songs.routes.get_song(db=db, range=range)