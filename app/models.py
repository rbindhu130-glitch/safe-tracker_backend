from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)


class Volunteer(Base):
    __tablename__ = "volunteers"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    mobile = Column(String)
    email = Column(String, unique=True, index=True) 
    address = Column(Text)
    availability = Column(String)
    id_proof_path = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    category = Column(String)
    description = Column(Text)
    photo_path = Column(String, nullable=True)
    contact = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

