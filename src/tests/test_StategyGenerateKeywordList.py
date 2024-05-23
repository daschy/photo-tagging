import os
import pytest
from src.models.ImageCRUD import ImageCRUD
from src.tests.test_utils.test_db_utils import clear_tables
from src.models.ReverseGeotagging import ReverseGeotagging
from src.models.AIGenTokenClassificationBert import AIGenTokenClassificationBert
from src.models.AIGenPaliGemma import AIGenPaliGemma
from src.models.StrategyGenerateKeywordList import StrategyGenerateKeywordList


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

    save_output = await self.strategy.generate_keyword_list_directory(
      root_dir=directory_path
    )
    
    await clear_tables(engine=self.strategy.db_engine)
    assert save_output
