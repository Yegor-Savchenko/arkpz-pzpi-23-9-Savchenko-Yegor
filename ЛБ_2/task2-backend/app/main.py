from sqlalchemy.orm import selectinload
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import engine, get_db
from app.models import Base
from app import models, schemas


app = FastAPI(
    title="Pet Health Monitoring API",
    version="1.0.0",
    description="API для моніторингу здоров'я домашніх тварин (ЛБ2).",
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/users")
async def create_user(
    user: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
):
    new_user = models.User(email=user.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email}


@app.post("/pets")
async def create_pet(
    pet: schemas.PetCreate,
    db: AsyncSession = Depends(get_db),
):
    new_pet = models.Pet(**pet.dict())
    db.add(new_pet)
    await db.commit()
    await db.refresh(new_pet)
    return {"id": new_pet.id, "name": new_pet.name}


@app.post("/health-records")
async def create_health_record(
    record: schemas.HealthRecordCreate,
    db: AsyncSession = Depends(get_db),
):
    new_record = models.HealthRecord(**record.dict())
    db.add(new_record)
    await db.commit()
    return {"status": "record added"}


@app.get("/pets/{pet_id}")
async def get_pet(pet_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Pet)
        .options(selectinload(models.Pet.records))
        .where(models.Pet.id == pet_id)
    )
    pet = result.scalar_one_or_none()

    if not pet:
        return {"error": "Pet not found"}

    return {
        "id": pet.id,
        "name": pet.name,
        "species": pet.species,
        "records": [
            {
                "created_at": r.created_at,
                "temperature_c": r.temperature_c,
                "activity_level": r.activity_level,
                "appetite_level": r.appetite_level,
            }
            for r in pet.records
        ],
    }

