from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
	create_async_engine,
	AsyncSession,
	AsyncEngine,
	async_sessionmaker,
)
import contextlib
from sqlalchemy.orm import sessionmaker

from models.orm.BaseOrm import BaseOrm


def get_db_session(engine) -> sessionmaker:
	db_session_maker = sessionmaker(
		bind=engine,
		class_=AsyncSession,
		expire_on_commit=False,
	)
	return db_session_maker


async def create_engine(db_connection_string: str) -> AsyncEngine:
	try:
		engine = create_async_engine(
			db_connection_string,
			echo=False,
			# future=True,
		)
		async with engine.begin() as conn:
			await conn.run_sync(BaseOrm.metadata.create_all)
		return engine
	except Exception as _:
		raise


@contextlib.asynccontextmanager
async def get_db_async_session(
	engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession]:
	db_session_maker = async_sessionmaker(
		bind=engine,
		class_=AsyncSession,
		expire_on_commit=False,
	)
	async with db_session_maker() as session:
		yield session
		await session.close()


@contextlib.asynccontextmanager
async def get_async_engine(
	db_connection_string: str,
):
	engine = create_async_engine(
		db_connection_string,
		echo=False,
		# future=True,
	)
	async with engine.begin() as conn:
		await conn.run_sync(BaseOrm.metadata.create_all)
	yield engine
	await engine.dispose()
