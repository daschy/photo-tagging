import os
import pytest
from src.models.ImageCRUD import ImageCRUD
from src.models.orm.Photo import Photo
from src.models.orm.CrudBase import CRUDBase
from src.tests.test_utils.test_utils import clear_tables, get_all_file_dir
from src.models.ReverseGeotagging import ReverseGeotagging
from src.models.AIGenTokenClassificationBert import AIGenTokenClassificationBert
from src.models.AIGenPaliGemma import AIGenPaliGemma
from src.models.StrategyGenerateKeywordList import StrategyGenerateKeywordList
from src.utils.db_utils_async import get_db_session


class TestStrategyGenerateKeywordList:
  strategy: StrategyGenerateKeywordList = None

  @classmethod
  def setup_class(cls):
    db_path = os.path.join(os.getcwd(), "src", "tests", "test_data", "test.db")
    cls.strategy = StrategyGenerateKeywordList(
      image_to_text_ai=AIGenPaliGemma(model_id="google/paligemma-3b-ft-cococap-448"),
      token_classification_ai=AIGenTokenClassificationBert(
        model_id="vblagoje/bert-english-uncased-finetuned-pos",
      ),
      reverse_geotagging=ReverseGeotagging(),
      db_path=f"sqlite+aiosqlite:////{db_path}",
    )

  @pytest.mark.asyncio
  async def test_generate_keyword_list_image(self):
    await self.strategy.init()
    image_path = os.path.join(
      os.getcwd(), "src", "tests", "test_data", "windmill_address_some_none.NEF"
    )
    keyword_list = await self.strategy.generate_keyword_list_image(
      image_path=image_path
    )
    assert len(keyword_list) > 0
    assert [
      "background",
      "black",
      "blue",
      "Meester Jac. Takkade",
      "Netherlands",
      "sky",
      "white",
      "windmill",
    ] == keyword_list

  @pytest.mark.asyncio
  async def test_save_to_db(self):
    await self.strategy.init()
    image_path = os.path.join(
      os.getcwd(), "src", "tests", "test_data", "windmill_address_some_none.NEF"
    )
    keyword_list = [
      "background",
      "black",
      "blue",
      "Meester Jac. Takkade",
      "Netherlands",
      "sky",
      "white",
      "windmill",
    ]
    save_output = await self.strategy.save_to_db(
      image_path=image_path, keyword_list=keyword_list
    )
    await clear_tables(engine=self.strategy.db_engine)
    assert save_output

  @pytest.mark.asyncio
  async def test_save_to_file(self):
    await self.strategy.init()
    image_path = os.path.join(
      os.getcwd(), "src", "tests", "test_data", "windmill_address_some_none.NEF"
    )
    keyword_list = [
      "background",
      "black",
      "blue",
      "Meester Jac. Takkade",
      "Netherlands",
      "sky",
      "white",
      "windmill",
    ]
    save_output = await self.strategy.save_to_file(
      image_path=image_path, keyword_list=keyword_list
    )
    assert save_output
    keyword_list_read_from_file = await self.strategy.image_crud.read_keyword_list(
      image_path
    )
    assert len(keyword_list) == len(keyword_list_read_from_file)
    assert keyword_list == keyword_list_read_from_file

  @pytest.mark.asyncio
  async def test_generate_keyword_list_directory_do_save_on_db_only(self):
    await self.strategy.init()
    directory_path = os.path.join(os.getcwd(), "src", "tests", "test_data")
    extension_list = ["nef"]
    save_output = await self.strategy.generate_keyword_list_directory(
      root_dir=directory_path, extension_list=extension_list
    )
    assert save_output
    image_path_list = get_all_file_dir(
      directory_path=directory_path, extension=extension_list[0]
    )
    session = get_db_session(self.strategy.db_engine)
    async with session() as db:
      photo_crud = CRUDBase(Photo)
      saved_entries = await photo_crud.get_all(db)
      assert len(saved_entries) == len(image_path_list)

    image_path_list = get_all_file_dir(
      directory_path=directory_path, extension=extension_list[0]
    )

    image_crud = ImageCRUD()
    for image_path in image_path_list:
      file_keyword_list = await image_crud.read_keyword_list(image_path=image_path)
      assert len(file_keyword_list) == 0

    await clear_tables(engine=self.strategy.db_engine)
    for image_path in image_path_list:
      await image_crud.delete_all_keyword_list(file_path=image_path)

  @pytest.mark.asyncio
  async def test_generate_keyword_list_directory_do_not_save_on_neither(self):
    await self.strategy.init()
    directory_path = os.path.join(os.getcwd(), "src", "tests", "test_data")
    extension_list = ["nef"]
    save_output = await self.strategy.generate_keyword_list_directory(
      root_dir=directory_path,
      extension_list=extension_list,
      save_on_db=False,
      save_on_file=False,
    )
    assert save_output

    image_path_list = get_all_file_dir(
      directory_path=directory_path, extension=extension_list[0]
    )
    session = get_db_session(self.strategy.db_engine)
    async with session() as db:
      photo_crud = CRUDBase(Photo)
      saved_entries = await photo_crud.get_all(db)

    assert len(saved_entries) == 0

    image_crud = ImageCRUD()
    for image_path in image_path_list:
      file_keyword_list = await image_crud.read_keyword_list(image_path=image_path)
      assert len(file_keyword_list) == 0

    await clear_tables(engine=self.strategy.db_engine)
    for image_path in image_path_list:
      await image_crud.delete_all_keyword_list(file_path=image_path)

  @pytest.mark.asyncio
  async def test_generate_keyword_list_directory_do_save_on_both(self):
    await self.strategy.init()
    directory_path = os.path.join(os.getcwd(), "src", "tests", "test_data")
    extension_list = ["nef"]
    save_output = await self.strategy.generate_keyword_list_directory(
      root_dir=directory_path,
      extension_list=extension_list,
      save_on_db=True,
      save_on_file=True,
    )
    assert save_output

    image_path_list = get_all_file_dir(
      directory_path=directory_path, extension=extension_list[0]
    )
    session = get_db_session(self.strategy.db_engine)
    async with session() as db:
      photo_crud = CRUDBase(Photo)
      saved_entries = await photo_crud.get_all(db)
    assert len(saved_entries) == len(image_path_list)
    image_crud = ImageCRUD()
    for image_path in image_path_list:
      file_keyword_list = await image_crud.read_keyword_list(image_path=image_path)
      photo_entry = next(x for x in saved_entries if x.path == image_path)
      assert len(file_keyword_list) == len(photo_entry.keyword_list)
      assert file_keyword_list == photo_entry.keyword_list

    await clear_tables(engine=self.strategy.db_engine)
    for image_path in image_path_list:
      await image_crud.delete_all_keyword_list(file_path=image_path)

  @pytest.mark.asyncio
  async def test_generate_keyword_list_directory_do_save_on_file_only(self):
    await self.strategy.init()
    directory_path = os.path.join(os.getcwd(), "src", "tests", "test_data")
    extension_list = ["nef"]
    save_output = await self.strategy.generate_keyword_list_directory(
      root_dir=directory_path,
      extension_list=extension_list,
      save_on_db=False,
      save_on_file=True,
    )
    assert save_output

    image_path_list = get_all_file_dir(
      directory_path=directory_path, extension=extension_list[0]
    )
    session = get_db_session(self.strategy.db_engine)
    async with session() as db:
      photo_crud = CRUDBase(Photo)
      saved_entries = await photo_crud.get_all(db)
    assert len(saved_entries) == 0

    image_crud = ImageCRUD()
    for image_path in image_path_list:
      file_keyword_list = await image_crud.read_keyword_list(image_path=image_path)
      assert len(file_keyword_list) > 0

    await clear_tables(engine=self.strategy.db_engine)
