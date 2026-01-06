from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    email: str


class PetCreate(BaseModel):
    owner_id: int
    name: str
    species: str
    age_years: Optional[int] = None
    weight_kg: Optional[float] = None


class HealthRecordCreate(BaseModel):
    pet_id: int
    temperature_c: Optional[float] = None
    activity_level: Optional[int] = None
    appetite_level: Optional[int] = None


class HealthRecordOut(BaseModel):
    created_at: datetime
    temperature_c: Optional[float]
    activity_level: Optional[int]
    appetite_level: Optional[int]


class PetOut(BaseModel):
    id: int
    name: str
    species: str
    records: List[HealthRecordOut]
