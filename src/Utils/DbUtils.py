import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from Models.BaseOrm import BaseOrm
from Logger.LoggerUtils import GetLogger

log = GetLogger(__name__)

# SQLite connection
DATABASE_URL = os.environ.get("DATABASE_URL")
log.info(f"DB URL = {DATABASE_URL}")

engine = create_async_engine(DATABASE_URL, echo=True)


AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# Create the tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.create_all)


# Dependency for creating a session
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
