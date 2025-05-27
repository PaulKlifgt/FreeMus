from pydantic import BaseModel


class SongGet(BaseModel):
    id: int


class SongCreate(BaseModel):
    name: str