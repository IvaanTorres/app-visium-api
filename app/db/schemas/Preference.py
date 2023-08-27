from sqlalchemy import create_engine, Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from ..config import Base

class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    locale = Column(String(length=10))
    welcomingMessageSize = Column(Integer, default=40)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="preferences")