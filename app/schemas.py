from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UserDTO(BaseModel):
    id: int
    login: str
    password: str


class TokenGet(Token):
    pass

class UserLogin(BaseModel):
    login: str
    password: str