from .base import Base
from sqlalchemy import Column, Integer, String, Boolean

class UsersModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    user_role = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
