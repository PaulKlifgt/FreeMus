from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

# Определяем модель Song
class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    file_path = Column(String, index=True)
    is_download = Column(Boolean, index=True)
    length = Column(Integer, default=0) # продолжительность в секундах
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", foreign_keys=[author_id], back_populates="songs")