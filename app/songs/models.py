from sqlalchemy import Column, Integer, String, Boolean
from database import Base

# Определяем модель Song
class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    file_path = Column(String, index=True)
    