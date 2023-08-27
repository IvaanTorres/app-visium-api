from sqlalchemy import create_engine, Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from ..config import Base

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(length=255)) 
    is_revoked = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tokens")