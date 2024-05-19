# crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Models.Photo import Photo, AsyncSessionLocal
from Utils.DbUtils import AsyncSession


async def get_photo(db: AsyncSession, photo_id: int):
    result = await db.execute(select(Photo).filter(Photo.id == photo_id))
    return result.scalars().first()


async def get_photos(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Photo).offset(skip).limit(limit))
    return result.scalars().all()


async def create_photo(db: AsyncSession, title: str, description: str):
    db_photo = Photo(title=title, description=description)
    db.add(db_photo)
    await db.commit()
    await db.refresh(db_photo)
    return db_photo


async def delete_photo(db: AsyncSession, photo_id: int):
    db_photo = await get_photo(db, photo_id)
    if db_photo:
        await db.delete(db_photo)
        await db.commit()


async def update_photo(db: AsyncSession, photo_id: int, title: str, description: str):
    db_photo = await get_photo(db, photo_id)
    if db_photo:
        db_photo.title = title
        db_photo.description = description
        await db.commit()
        await db.refresh(db_photo)
    return db_photo


# Dependency for creating a session
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
