from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Text

from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    # email = Column(String(50), unique=True, index=True)
    # hashed_password = Column(String(100))
    # is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # deleted_at = Column(DateTime, nullable=True)
