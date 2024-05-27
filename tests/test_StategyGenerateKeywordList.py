import os
import glob
import pytest
import pytest_asyncio
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from models.ExifFileCRUD import ExifFileCRUD
from models.orm.Photo import Photo
from models.DBCRUD import DBCRUD
from models.orm.BaseOrm import BaseOrm
from models.StrategyGenerateKeywordList import (
	StrategyGenerateKeywordList,
)
from utils.db_utils_async import get_db_session, init_engine
from tests.test_utils.test_utils import get_all_file_dir


class TestStrategyGenerateKeywordList:
	test_image_path: str = os.path.join(
		os.getcwd(), "tests", "test_data", "windmill_address_some_none.NEF"
	)
	test_keyword_list = [
		"background",
		"black",
		"blue",
		"Meester Jac. Takkade",
		"Netherlands",
		"sky",
		"white",
		"windmill",
	]
	test_directory_with_photos_path: str = os.path.join(os.getcwd(), "tests", "test_data")
	test_extension_list = ["nef"]

	@pytest_asyncio.fixture(scope="function")
	async def test_db(self, strategy: StrategyGenerateKeywordList):
		test_db_path: str = os.path.join(
			self.test_directory_with_photos_path, strategy.get_db_name()
		)
		test_db_conn_str: str = f"sqlite+aiosqlite:////{test_db_path}"
		engine = await init_engine(test_db_conn_str)
		sessionmaker = get_db_session(engine=engine)
		session = sessionmaker()
		yield session
		async with engine.begin() as conn:
			await conn.run_sync(BaseOrm.metadata.drop_all)

	@pytest.fixture(scope="class")
	def exif_crud(self):
		exif_crud = ExifFileCRUD()
		yield exif_crud

	@pytest_asyncio.fixture(scope="function")
	async def file_path_list(self, exif_crud: ExifFileCRUD):
		output = get_all_file_dir(
			directory_path=self.test_directory_with_photos_path,
			extension=self.test_extension_list[0],
		)
		for image_path in output:
			await exif_crud.delete_all_keyword_list(file_path=image_path)
		yield output

	@pytest.mark.asyncio
	async def test_generate_keyword_list_image(
		self, strategy: StrategyGenerateKeywordList
	):
		keyword_list = await strategy.generate_keyword_list_image(
			image_path=self.test_image_path
		)
		assert len(keyword_list) > 0
		assert keyword_list == self.test_keyword_list

	@pytest.mark.asyncio
	async def test_save_to_db(
		self, strategy: StrategyGenerateKeywordList, test_db: AsyncSession
	):
		await strategy.save_to_db(
			db=test_db, image_path=self.test_image_path, keyword_list=self.test_keyword_list
		)
		saved_entries: List[Photo] = await self.retrieve_test_db_entries(db=test_db)
		assert len(saved_entries) == 1
		assert saved_entries[0].keyword_list == self.test_keyword_list  # type: ignore

	@pytest.mark.asyncio
	async def test_save_to_file(self, strategy: StrategyGenerateKeywordList):
		save_output = await strategy.save_to_file(
			file_path=self.test_image_path, keyword_list=self.test_keyword_list
		)
		assert save_output
		keyword_list_read_from_file = await strategy.exif_crud.read_keyword_list(
			self.test_image_path
		)
		assert len(self.test_keyword_list) == len(keyword_list_read_from_file)
		assert self.test_keyword_list == keyword_list_read_from_file

	async def retrieve_test_db_entries(self, db: AsyncSession) -> list:
		# session = get_db_session(db)
		# async with session() as db:
		photo_crud = DBCRUD(Photo)
		saved_entries = await photo_crud.get_all(db)
		return saved_entries

	@pytest.mark.asyncio
	async def test_generate_keyword_list_directory_do_save_on_db_only(
		self,
		strategy: StrategyGenerateKeywordList,
		file_path_list: List[str],
		test_db: AsyncSession,
		exif_crud: ExifFileCRUD,
	):
		save_output = await strategy.generate_keyword_list_directory(
			directory_path=self.test_directory_with_photos_path,
			extension_list=self.test_extension_list,
		)
		assert save_output
		saved_entries: List[Photo] = await self.retrieve_test_db_entries(db=test_db)
		assert len(saved_entries) == len(file_path_list)
		for image_path in file_path_list:
			file_keyword_list = await exif_crud.read_keyword_list(file_path=image_path)
			assert len(file_keyword_list) == 0

	@pytest.mark.asyncio
	async def test_generate_keyword_list_directory_do_not_save_on_neither(
		self,
		strategy: StrategyGenerateKeywordList,
		file_path_list: List[str],
		test_db: AsyncSession,
		exif_crud: ExifFileCRUD,
	):
		save_output = await strategy.generate_keyword_list_directory(
			directory_path=self.test_directory_with_photos_path,
			extension_list=self.test_extension_list,
			save_on_db=False,
			save_on_file=False,
		)
		assert save_output

		saved_entries = await self.retrieve_test_db_entries(db=test_db)
		assert len(saved_entries) == 0
		for image_path in file_path_list:
			file_keyword_list = await exif_crud.read_keyword_list(file_path=image_path)
			assert len(file_keyword_list) == 0

	@pytest.mark.asyncio
	async def test_generate_keyword_list_directory_do_save_on_both(
		self,
		strategy: StrategyGenerateKeywordList,
		file_path_list: List[str],
		test_db: AsyncSession,
		exif_crud: ExifFileCRUD,
	):
		save_output = await strategy.generate_keyword_list_directory(
			directory_path=self.test_directory_with_photos_path,
			extension_list=self.test_extension_list,
			save_on_db=True,
			save_on_file=True,
		)
		assert save_output

		saved_entries = await self.retrieve_test_db_entries(db=test_db)
		assert len(saved_entries) == len(file_path_list)
		for file_path in file_path_list:
			file_keyword_list = await exif_crud.read_keyword_list(file_path=file_path)
			photo_entry = next(x for x in saved_entries if x.path == file_path)
			assert len(file_keyword_list) == len(photo_entry.keyword_list)
			assert file_keyword_list == photo_entry.keyword_list

	@pytest.mark.asyncio
	async def test_generate_keyword_list_directory_do_save_on_file_only(
		self,
		strategy: StrategyGenerateKeywordList,
		file_path_list: List[str],
		test_db: AsyncSession,
		exif_crud: ExifFileCRUD,
	):
		save_output = await strategy.generate_keyword_list_directory(
			directory_path=self.test_directory_with_photos_path,
			extension_list=self.test_extension_list,
			save_on_db=False,
			save_on_file=True,
		)
		assert save_output

		saved_entries: List[Photo] = await self.retrieve_test_db_entries(db=test_db)
		assert len(saved_entries) == 0
		for image_path in file_path_list:
			file_keyword_list = await exif_crud.read_keyword_list(file_path=image_path)
			assert len(file_keyword_list) > 0
