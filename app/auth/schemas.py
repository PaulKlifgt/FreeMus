from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UserDTO(BaseModel):
    id: int
    username: str
    password: str


class TokenGet(Token):
    pass

class UserLogin(BaseModel):
    username: str
    password: str