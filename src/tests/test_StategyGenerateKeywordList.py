import os
import pytest
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
    cls.strategy = StrategyGenerateKeywordList(
      image_to_text_ai=AIGenPaliGemma(model_id="google/paligemma-3b-ft-cococap-448"),
      token_classification_ai=AIGenTokenClassificationBert(
        model_id="vblagoje/bert-english-uncased-finetuned-pos",
      ),
      reverse_geotagging=ReverseGeotagging(),
      db_path=f"sqlite+aiosqlite:////{os.getcwd()}/src/tests/test_data/test.db",
    )

  @pytest.mark.asyncio
  async def test_generate_keyword_list_image(self):
    await self.strategy.init()
    image_path = f"{os.getcwd()}/src/tests/test_data/windmill_address_some_none.NEF"
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
    image_path = f"{os.getcwd()}/src/tests/test_data/windmill_address_some_none.NEF"
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
    image_path = f"{os.getcwd()}/src/tests/test_data/windmill_address_some_none.NEF"
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
  async def test_generate_keyword_list_directory(self):
    await self.strategy.init()
    directory_path = f"{os.getcwd()}/src/tests/test_data"
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

    await clear_tables(engine=self.strategy.db_engine)
