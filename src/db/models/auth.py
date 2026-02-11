from sqlalchemy import Column, Integer, String, ForeignKey
from src.db.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(50), nullable=False, unique=True)