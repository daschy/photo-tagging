from collections.abc import AsyncGenerator, Callable
import os
from unittest.mock import MagicMock
import pytest
import pytest_asyncio
from models.AIGenBert import AIGenBert
from models.AIGenPaliGemma import AIGenPaliGemma
from models.DBCRUD import DBCRUD
from models.orm.Image import Image
from services.StrategyImageGenerateImageDescription import (
	StrategyGenerateImageDescription,
)
from src.utils.db_utils_async import (
	create_engine,
	get_db_session,
	get_async_engine,
	get_db_async_session,
)


test_image_path: str = os.path.join(
	os.getcwd(), "tests", "test_data", "windmill_address_some_none.NEF"
)
test_directory_with_photos_path: str = os.path.join(os.getcwd(), "tests", "test_data")
test_extension_list = ["nef"]


@pytest_asyncio.fixture(scope="function")
async def strategy(
	mock_ai_gen_paligemma_list: tuple[
		Callable[[], AIGenPaliGemma], Callable[[], AIGenPaliGemma]
	],
	mock_ai_gen_bert: AIGenBert,
) -> AsyncGenerator[StrategyGenerateImageDescription]:
	output = StrategyGenerateImageDescription(
		ai_gen_list_for_description=[
			mock_ai_gen_paligemma_list[0](),
			mock_ai_gen_paligemma_list[1](),
		],
		ai_gen_tokenization=mock_ai_gen_bert,
		db_connection_string="sqlite+aiosqlite:///:memory:",
	)
	yield output


@pytest.mark.asyncio
async def test_file_do_not_exists(strategy: StrategyGenerateImageDescription):
	image_to_process = "file do not exists"

	with pytest.raises(FileNotFoundError):
		await strategy.process_file(image_path=image_to_process, db_session=MagicMock())


@pytest.mark.asyncio
async def test_should_gen_description_for_one_file(
	test_keyword_list_colors: list[str],
	test_keyword_list_caption: list[str],
	strategy: StrategyGenerateImageDescription,
):
	image_to_process = test_image_path

	description = await strategy.process_file(
		image_path=image_to_process, db_session=None
	)

	assert description == list(
		sorted(test_keyword_list_caption + test_keyword_list_colors)
	)


@pytest.mark.asyncio
async def test_should_save_file_description_to_db(
	test_keyword_list_colors: list[str],
	test_keyword_list_caption: list[str],
	strategy: StrategyGenerateImageDescription,
):
	image_to_process = test_image_path
	async with get_async_engine(strategy.db_connection_string) as db_engine:
		async with get_db_async_session(db_engine) as session:
			await strategy.process_file(
				image_path=image_to_process,
				db_session=session,
			)
			image = await DBCRUD(Image).get_by(session, file_path=test_image_path)
			assert image.keyword_list_description == (
				list(sorted(test_keyword_list_caption + test_keyword_list_colors))
			)  # type: ignore
