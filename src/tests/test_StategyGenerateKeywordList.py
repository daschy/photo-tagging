import os
import pytest
from src.tests.test_utils.test_db_utils import get_db_engine_and_session, clear_tables
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
      db_path=f"sqlite+aiosqlite:////{os.getcwd()}/src/tests/test_images/test.db",
    )

  @pytest.mark.asyncio
  async def test_generate_keyword_list_image(self):
    await self.strategy.init()
    image_path = f"{os.getcwd()}/src/tests/test_images/windmill_address_some_none.NEF"
    keyword_list = await self.strategy.generate_keyword_list_image(
      image_path=image_path
    )
    assert len(keyword_list) > 0
    assert [
      "Meester Jac. Takkade",
      "Netherlands",
      "background",
      "black",
      "blue",
      "sky",
      "white",
      "windmill",
    ] == keyword_list

  @pytest.mark.asyncio
  async def test_save_keyword_list_image(self):
    await self.strategy.init()
    image_path = f"{os.getcwd()}/src/tests/test_images/windmill_address_some_none.NEF"
    keyword_list = [
      "Meester Jac. Takkade",
      "Netherlands",
      "background",
      "black",
      "blue",
      "sky",
      "white",
      "windmill",
    ]
    save_output = await self.strategy.save_to_db(
      image_path=image_path, keyword_list=keyword_list
    )
    await clear_tables(engine=self.strategy.db_engine)
    assert save_output
