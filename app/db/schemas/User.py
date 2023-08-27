from sqlalchemy import create_engine, Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from ..config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String(length=100))
    email = Column(String, index=True)

    tokens = relationship("Token", back_populates="user")
    logins = relationship("Login", back_populates="user")
    preferences = relationship("Preference", back_populates="user")