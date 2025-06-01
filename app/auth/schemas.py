from pydantic import BaseModel
from typing import Annotated
from fastapi import Form


class Token(BaseModel):
    access_token: str
    token_type: str


class UserDTO(BaseModel):
    id: int
    username: str
    password: str


class TokenGet(Token):
    pass


class UserLogin:
    def __init__(self, 
            username: Annotated[str, Form()],
            password: Annotated[str, Form()]
            ):
        self.username = username
        self.password = password

