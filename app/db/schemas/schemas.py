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

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(length=100)) 
    is_revoked = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tokens")

class Login(Base):
    __tablename__ = "logins"

    id = Column(Integer, primary_key=True, index=True)
    nb_logins = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="logins")

class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    locale = Column(String(length=10))
    welcomingMessageSize = Column(Integer, default=40)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="preferences")
