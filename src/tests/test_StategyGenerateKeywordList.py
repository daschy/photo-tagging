import os
import pytest
import pytest_asyncio
from typing import List
from src.models.ImageCRUD import ImageCRUD
from src.models.orm.Photo import Photo
from src.models.orm.CrudBase import CRUDBase
from src.models.orm.BaseOrm import BaseOrm
from src.tests.test_utils.test_utils import get_all_file_dir
from src.models.ReverseGeotagging import ReverseGeotagging
from src.models.AIGenPipeline import AIGenPipeline
from src.models.AIGenPretrained import AIGenPretrained
from src.models.StrategyGenerateKeywordList import StrategyGenerateKeywordList
from src.utils.db_utils_async import get_db_session


class TestStrategyGenerateKeywordList:
  test_image_path: str = os.path.join(
    os.getcwd(), "src", "tests", "test_data", "windmill_address_some_none.NEF"
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
  test_data_path: str = os.path.join(os.getcwd(), "src", "tests", "test_data")
  test_extension_list = ["nef"]
  test_db_path = os.path.join(os.getcwd(), "src", "tests", "test_data", "test.db")

  @pytest_asyncio.fixture(scope="function")
  async def strategy(self):
    output = StrategyGenerateKeywordList(
      image_to_text_ai=AIGenPretrained(model_id="google/paligemma-3b-ft-cococap-448"),
      token_classification_ai=AIGenPipeline(
        model_id="vblagoje/bert-english-uncased-finetuned-pos"
      ),
      reverse_geotagging=ReverseGeotagging(),
      db_path=f"sqlite+aiosqlite:////{self.test_db_path}",
    )
    await output.init()
    yield output
    async with output.db_engine.begin() as conn:
      await conn.run_sync(BaseOrm.metadata.drop_all)

  @pytest_asyncio.fixture(scope="function")
  async def file_path_list(self):
    output = get_all_file_dir(
      directory_path=self.test_data_path, extension=self.test_extension_list[0]
    )
    image_crud = ImageCRUD()
    for image_path in output:
      await image_crud.delete_all_keyword_list(file_path=image_path)
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
  async def test_save_to_db(self, strategy: StrategyGenerateKeywordList):
    save_output = await strategy.save_to_db(
      image_path=self.test_image_path, keyword_list=self.test_keyword_list
    )
    assert save_output

  @pytest.mark.asyncio
  async def test_save_to_file(self, strategy: StrategyGenerateKeywordList):
    save_output = await strategy.save_to_file(
      image_path=self.test_image_path, keyword_list=self.test_keyword_list
    )
    assert save_output
    keyword_list_read_from_file = await strategy.image_crud.read_keyword_list(
      self.test_image_path
    )
    assert len(self.test_keyword_list) == len(keyword_list_read_from_file)
    assert self.test_keyword_list == keyword_list_read_from_file

  async def validate_db_entries(self, db_engine, expected_count: int):
    session = get_db_session(db_engine)
    async with session() as db:
      photo_crud = CRUDBase(Photo)
      saved_entries = await photo_crud.get_all(db)
      assert len(saved_entries) == expected_count
      return saved_entries

  @pytest.mark.asyncio
  async def test_generate_keyword_list_directory_do_save_on_db_only(
    self, strategy: StrategyGenerateKeywordList, file_path_list: List[str]
  ):
    save_output = await strategy.generate_keyword_list_directory(
      root_dir=self.test_data_path, extension_list=self.test_extension_list
    )
    assert save_output
    await self.validate_db_entries(
      db_engine=strategy.db_engine, expected_count=len(file_path_list)
    )
    image_crud = ImageCRUD()
    for image_path in file_path_list:
      file_keyword_list = await image_crud.read_keyword_list(file_path=image_path)
      assert len(file_keyword_list) == 0

  @pytest.mark.asyncio
  async def test_generate_keyword_list_directory_do_not_save_on_neither(
    self, strategy: StrategyGenerateKeywordList, file_path_list: List[str]
  ):
    save_output = await strategy.generate_keyword_list_directory(
      root_dir=self.test_data_path,
      extension_list=self.test_extension_list,
      save_on_db=False,
      save_on_file=False,
    )
    assert save_output

    await self.validate_db_entries(db_engine=strategy.db_engine, expected_count=0)
    image_crud = ImageCRUD()
    for image_path in file_path_list:
      file_keyword_list = await image_crud.read_keyword_list(file_path=image_path)
      assert len(file_keyword_list) == 0

  @pytest.mark.asyncio
  async def test_generate_keyword_list_directory_do_save_on_both(
    self, strategy: StrategyGenerateKeywordList, file_path_list: List[str]
  ):
    save_output = await strategy.generate_keyword_list_directory(
      root_dir=self.test_data_path,
      extension_list=self.test_extension_list,
      save_on_db=True,
      save_on_file=True,
    )
    assert save_output

    saved_entries = await self.validate_db_entries(
      db_engine=strategy.db_engine, expected_count=len(file_path_list)
    )

    image_crud = ImageCRUD()
    for file_path in file_path_list:
      file_keyword_list = await image_crud.read_keyword_list(file_path=file_path)
      photo_entry = next(x for x in saved_entries if x.path == file_path)
      assert len(file_keyword_list) == len(photo_entry.keyword_list)
      assert file_keyword_list == photo_entry.keyword_list

  @pytest.mark.asyncio
  async def test_generate_keyword_list_directory_do_save_on_file_only(
    self, strategy: StrategyGenerateKeywordList, file_path_list: List[str]
  ):
    save_output = await strategy.generate_keyword_list_directory(
      root_dir=self.test_data_path,
      extension_list=self.test_extension_list,
      save_on_db=False,
      save_on_file=True,
    )
    assert save_output

    await self.validate_db_entries(db_engine=strategy.db_engine, expected_count=0)
    image_crud = ImageCRUD()
    for image_path in file_path_list:
      file_keyword_list = await image_crud.read_keyword_list(file_path=image_path)
      assert len(file_keyword_list) > 0
