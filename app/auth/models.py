from sqlalchemy import Column, Integer, String, Boolean
from database import Base

# Определяем модель User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True)
    password = Column(String, index=True)
    