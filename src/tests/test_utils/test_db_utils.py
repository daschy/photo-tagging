from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

# from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.orm.BaseOrm import BaseOrm


async def get_db_engine_and_session(
  db_path: str,
) -> [
  AsyncSession,
  AsyncEngine,
]:  # type: ignore
  db_engine: AsyncEngine = create_async_engine(db_path, echo=True)
  # Create the tables
  async with db_engine.begin() as conn:
    await conn.run_sync(BaseOrm.metadata.create_all)
  db_session = sessionmaker(bind=db_engine, class_=AsyncSession, expire_on_commit=False)
  return db_session, db_engine


async def clear_tables(engine: AsyncEngine) -> None:
  async with engine.begin() as conn:
    await conn.run_sync(BaseOrm.metadata.drop_all)
