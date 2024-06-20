import os
import pytest
import pytest_asyncio
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from models.ExifFileCRUD import ExifFileCRUD
from models.orm.Photo import Photo
from models.DBCRUD import DBCRUD
from models.StrategyGenerateKeywordList import (
	StrategyGenerateKeywordList,
)

from utils.db_utils_async import get_db_session, create_engine
from tests.test_utils.test_utils import get_all_file_dir


test_image_path: str = os.path.join(
	os.getcwd(), "tests", "test_data", "windmill_address_some_none.NEF"
)
test_directory_with_photos_path: str = os.path.join(os.getcwd(), "tests", "test_data")
test_extension_list = ["nef"]


@pytest_asyncio.fixture(scope="function")
async def file_path_list(exif_crud: ExifFileCRUD):
	output = get_all_file_dir(
		directory_path=test_directory_with_photos_path,
		extension=test_extension_list[0],
	)
	for image_path in output:
		await exif_crud.delete_keyword_list(file_path=image_path)
	yield output


@pytest_asyncio.fixture(scope="function")
async def test_db(
	strategy_gen_keyword_list: StrategyGenerateKeywordList,
):
	test_db_path: str = os.path.join(
		test_directory_with_photos_path, strategy_gen_keyword_list.get_db_name()
	)
	if os.path.exists(test_db_path):
		os.remove(test_db_path)
	test_db_conn_str: str = f"sqlite+aiosqlite:////{test_db_path}"
	engine = await create_engine(test_db_conn_str)
	sessionmaker = get_db_session(engine=engine)
	session: AsyncSession = sessionmaker()
	yield session
	await session.close()
	if os.path.exists(test_db_path):
		os.remove(test_db_path)


async def retrieve_test_db_entries(db: AsyncSession) -> list:
	# session = get_db_session(db)
	# async with session() as db:
	photo_crud = DBCRUD(Photo)
	saved_entries = await photo_crud.get_all(db)
	return saved_entries


@pytest.mark.asyncio
async def test_generate_keyword_list_single_file(
	strategy_gen_keyword_list: StrategyGenerateKeywordList,
	test_keyword_list: List[str],
):
	keyword_list = await strategy_gen_keyword_list.generate_keyword_list_image(
		image_path=test_image_path
	)
	assert len(keyword_list) == len(test_keyword_list)
	assert keyword_list == test_keyword_list


@pytest.mark.asyncio
async def test_save_keyword_list_to_db(
	strategy_gen_keyword_list: StrategyGenerateKeywordList,
	test_db: AsyncSession,
	test_keyword_list: List[str],
):
	await strategy_gen_keyword_list.save_to_db(
		db=test_db, image_path=test_image_path, keyword_list=test_keyword_list
	)
	saved_entries: List[Photo] = await retrieve_test_db_entries(db=test_db)
	assert len(saved_entries) == 1
	assert saved_entries[0].keyword_list == test_keyword_list  # type: ignore


@pytest.mark.asyncio
async def test_save_keyword_list_to_file(
	# self,
	strategy_gen_keyword_list: StrategyGenerateKeywordList,
	test_keyword_list: List[str],
):
	save_output = await strategy_gen_keyword_list.save_to_file(
		file_path=test_image_path, keyword_list=test_keyword_list
	)
	assert save_output
	keyword_list_read_from_file = (
		await strategy_gen_keyword_list.exif_crud.read_keyword_list(test_image_path)
	)
	assert len(test_keyword_list) == len(keyword_list_read_from_file)
	assert test_keyword_list == keyword_list_read_from_file


@pytest.mark.asyncio
async def test_generate_keyword_list_for_directory_with_no_files(
	strategy_gen_keyword_list: StrategyGenerateKeywordList,
	test_keyword_list: List[str],
):
	pass


@pytest.mark.asyncio
async def test_generate_keyword_list_for_directory_and_save_to_db_only(
	# self,
	strategy_gen_keyword_list: StrategyGenerateKeywordList,
	file_path_list: List[str],
	test_db: AsyncSession,
	exif_crud: ExifFileCRUD,
):
	save_output = await strategy_gen_keyword_list.generate_keyword_list_directory(
		directory_path=test_directory_with_photos_path,
		extension_list=test_extension_list,
		save_on_file=False,
	)
	assert save_output
	saved_entries: List[Photo] = await retrieve_test_db_entries(db=test_db)
	assert len(saved_entries) == len(file_path_list)
	for image_path in file_path_list:
		file_keyword_list = await exif_crud.read_keyword_list(file_path=image_path)
		assert len(file_keyword_list) == 0


@pytest.mark.asyncio
async def test_generate_keyword_list_directory_and_save_on_file_and_db(
	strategy_gen_keyword_list: StrategyGenerateKeywordList,
	file_path_list: List[str],
	test_db: AsyncSession,
	exif_crud: ExifFileCRUD,
):
	save_output = await strategy_gen_keyword_list.generate_keyword_list_directory(
		directory_path=test_directory_with_photos_path,
		extension_list=test_extension_list,
		save_on_file=True,
	)
	assert save_output

	saved_entries = await retrieve_test_db_entries(db=test_db)
	assert len(saved_entries) == len(file_path_list)
	for file_path in file_path_list:
		file_keyword_list = await exif_crud.read_keyword_list(file_path=file_path)
		photo_entry: Photo = next(x for x in saved_entries if x.path == file_path)
		assert len(file_keyword_list) == len(photo_entry.keyword_list)  # type: ignore
		assert file_keyword_list == photo_entry.keyword_list
