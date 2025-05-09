from pydantic import BaseModel


class SongGet(BaseModel):
    name: str
    author_name: str


class SongCreate(BaseModel):
    name: str