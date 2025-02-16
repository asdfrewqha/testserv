from sqlalchemy import Column, String

# from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    token = Column(String, nullable=False, unique=True)
