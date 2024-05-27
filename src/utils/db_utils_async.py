from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from models.orm.BaseOrm import BaseOrm


def get_db_session(engine) -> sessionmaker:
	db_session = sessionmaker(
		bind=engine,
		class_=AsyncSession,
		expire_on_commit=False,
	)
	return db_session


async def init_engine(db_connection_string: str) -> AsyncEngine:
	try:
		engine = create_async_engine(db_connection_string, echo=False)
		async with engine.begin() as conn:
			await conn.run_sync(BaseOrm.metadata.create_all)
		return engine
	except Exception as _:
		raise
