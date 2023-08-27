from sqlalchemy import create_engine, Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from ..config import Base

class Login(Base):
    __tablename__ = "logins"

    id = Column(Integer, primary_key=True, index=True)
    nb_logins = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="logins")