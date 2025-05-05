from pydantic import BaseModel


class SongGet(BaseModel):
    name: str