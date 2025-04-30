from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

# Определяем модель Task
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True)
    password = Column(String, index=True)
    