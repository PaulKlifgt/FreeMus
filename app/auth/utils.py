import jwt, hashlib

import settings
from . import  models

from sqlalchemy.orm import Session
from typing import Union
from fastapi import HTTPException, status
from jwt import InvalidTokenError


from .schemas import Token, UserDTO


class UserAuth():

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    invalide_name_or_password_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username_exists_exception = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Username already exists",
    )

    # хеширование
    def hash_password(self, password: str):
        return hashlib.sha256(password.encode()).hexdigest()
    

    def check_password(self, stored_password, provided_password):
        return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

    # проверка валидности юзера
    def validate_user(self, db: Session, login: str, password: str) -> Union[UserDTO, bool]:
        user: UserDTO = db.query(models.User).filter(models.User.login == login).first()
        if user and self.check_password(user.password, password):
            return user
        return False

    # создание токена
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy() #копируем данные для кодирования
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
        return encoded_jwt

    # авторизация
    def login_for_access_token(self, db: Session, login: str, password: str) -> Token:
        user: UserDTO = self.validate_user(db, login, password) #проверка введенных данных
      
        if not user:
            raise self.invalide_name_or_password_exception
      
        #данные для кодирования
        access_token = self.create_access_token(
            data={"login": user.login, "password": password}
        ) #создание токена
        return Token(access_token=access_token, token_type="bearer")
    
    # получение юзера по токену
    def get_current_user(self, db, token: str):

        try:
            # декодировка токена
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            #данные из токена
            login: str = payload.get("login")
            password: str = payload.get("password")

            #если в токене нет поля login
            if login is None:
                raise self.credentials_exception

        except InvalidTokenError:
            raise self.credentials_exception
        
        #проверка данных
        user = self.validate_user(db, login, password)
        if not user:
            raise self.invalide_name_or_password_exception
        return user
    
    # регистрация
    def register(self, db: Session, login: str, password: str):
        user_logined = db.query(models.User).filter(models.User.login == login).first()
        if user_logined:
            raise self.username_exists_exception
        user = models.User(login=login, password=self.hash_password(password))
        db.add(user)
        db.commit()
        db.refresh(user)
        return user