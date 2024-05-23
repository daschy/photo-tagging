from sqlalchemy.ext.asyncio import AsyncEngine

# from sqlalchemy import create_engine
from src.models.orm.BaseOrm import BaseOrm

async def clear_tables(engine: AsyncEngine) -> None:
  async with engine.begin() as conn:
    await conn.run_sync(BaseOrm.metadata.drop_all)
