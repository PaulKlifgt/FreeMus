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
    album_id = Column(Integer, ForeignKey("albums.id"))
    album = relationship("Album", foreign_keys=[album_id], back_populates="albums")


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_single = Column(Boolean, index=True)
    count_songs = Column(Integer, default=0)
    file_path = Column(String, index=True)
    length = Column(Integer, default=0) # продолжительность в секундах
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", foreign_keys=[author_id], back_populates="albums")
    songs = relationship("Song", back_populates="album")