
from sqlalchemy.orm import Session
from fastapi import APIRouter

from . import schemas, models

from .auth import UserAuth



#экземпляр класса
user_auth = UserAuth()


def login(db: Session, user: schemas.UserLogin):
    #получаем токен и возращаем клиент
    token = user_auth.login_for_access_token(db, user.login, user.password)
    return token


def read_me(db: Session, token: schemas.TokenGet):
    #декодируем токен и получаем обьект пользователя
    return user_auth.get_current_user(token=token.access_token, db=db)


def register(db: Session, user: schemas.UserLogin):
    user = models.User(login=user.login, password=user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user