
from sqlalchemy.orm import Session
from fastapi import APIRouter

from . import schemas

from . import models

from .utils import UserAuth



#экземпляр класса
user_auth = UserAuth()


async def login(db: Session, user: schemas.UserLogin):
    #получаем токен и возращаем клиент
    token = user_auth.login_for_access_token(db, user.login, user.password)
    return token


async def read_me(db: Session, token: schemas.TokenGet):
    #декодируем токен и получаем обьект пользователя
    return user_auth.get_current_user(token=token.access_token, db=db)


async def register(db: Session, user: schemas.UserLogin):
    return user_auth.register(db, user.login, user.password)