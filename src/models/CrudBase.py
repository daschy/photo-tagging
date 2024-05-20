# crud.py
from typing import Type, TypeVar, Generic, List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.BaseOrm import BaseOrm

T = TypeVar("T", bound=BaseOrm)


class CRUDBase(Generic[T]):
  def __init__(self, model: Type[T]):
    self.model = model

  async def get(self, db: AsyncSession, id: int) -> T:
    result = await db.execute(select(self.model).filter(self.model.id == id))
    return result.scalars().first()

  async def get_by(self, db: AsyncSession, **kwargs) -> T:
    query = select(self.model).filter_by(**kwargs)
    result = await db.execute(query)
    return result.scalars().first()

  async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[T]:
    result = await db.execute(select(self.model).offset(skip).limit(limit))
    return result.scalars().all()

  async def create(self, db: AsyncSession, obj_in: T) -> T:
    obj = await self.get(db, id=obj_in.id)
    if obj:
      return await self.update(db, id=obj_in.id, obj_in=obj_in)
    else:
      return await self._create(db, obj_in=obj_in)

  async def _create(self, db: AsyncSession, obj_in: T) -> T:
    db.add(obj_in)
    await db.commit()
    await db.refresh(obj_in)
    return obj_in

  async def update(self, db: AsyncSession, id: int, obj_in: T) -> T:
    result = await db.execute(select(self.model).filter(self.model.id == id))
    obj = result.scalars().first()
    if obj:
      for key, value in vars(obj_in).items():
        setattr(obj, key, value)
      await db.commit()
      await db.refresh(obj)  # Refresh the object in the current session
    return obj

  async def delete(self, db: AsyncSession, id: int) -> None:
    result = await db.execute(select(self.model).filter(self.model.id == id))
    obj = result.scalars().first()
    await db.delete(obj)
    await db.commit()
