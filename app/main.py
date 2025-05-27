from typing import Annotated, Optional
from fastapi import FastAPI, Depends, Header
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/") 


# регистрация
@app.post('/users/register/', tags=["Users"])
async def register(user: auth.schemas.UserLogin, db: Session = Depends(get_db)):
    return await auth.routes.register(user=user, db=db)


#авторизация
@app.post('/users/login/', tags=["Users"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    return await auth.routes.login(user=form_data, db=db)
    

#пример ручки для получения данных по токену
@app.get('/users/me/', tags=["Users"])
async def read_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)): #токен передается в headers
    return await auth.routes.get_user_by_token(token=token, db=db)


@app.get('/', tags=["Songs"])
async def main(db: Session = Depends(get_db)):
    data = '<!DOCTYPE html><html><head><title>FastAPI video streaming</title></head><body><audio width="1200" controls><source src="http://127.0.0.1:8000/get_song_streaming/" type="audio/mp3" /></audio></body></html>'

    return HTMLResponse(data)


@app.get('/get_song_streaming/', tags=["Songs"])
async def get_song_streaming(range: Optional[str] = Header(None), db: Session = Depends(get_db)):
    return await songs.routes.get_song_streaming(range=range, db=db)


@app.post('/create_song/', tags=["Songs"])
async def create_song(song: songs.schemas.SongCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await songs.routes.create_song(db=db, token=token, song=song)


@app.get('/get_song_info/', tags=["Songs"])
async def create_song(song_id: int, db: Session = Depends(get_db)):
    return await songs.routes.get_song_info(db=db, song_id=song_id)