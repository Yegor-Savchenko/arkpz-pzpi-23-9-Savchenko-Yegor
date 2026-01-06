from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)

    pets = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String(100), nullable=False)
    species = Column(String(50), nullable=False)
    age_years = Column(Integer, nullable=True)
    weight_kg = Column(Float, nullable=True)

    owner = relationship("User", back_populates="pets")
    records = relationship("HealthRecord", back_populates="pet", cascade="all, delete-orphan")


class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    temperature_c = Column(Float, nullable=True)
    activity_level = Column(Integer, nullable=True)  # 1..10
    appetite_level = Column(Integer, nullable=True)  # 1..10

    pet = relationship("Pet", back_populates="records")
