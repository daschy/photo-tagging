import os
import pytest

from src.models.ReverseGeotagging import ReverseGeotagging
from src.models.AIGenTokenClassificationBert import AIGenTokenClassificationBert
from src.models.AIGenPaliGemma import AIGenPaliGemma
from src.models.StrategyCalculateKeywordList import StrategyCalculateKeywordList


class TestStrategy:
  strategy: StrategyCalculateKeywordList = None

  @classmethod
  def setup_class(cls):
    cls.strategy = StrategyCalculateKeywordList(
      image_to_text_ai=AIGenPaliGemma(model_id="google/paligemma-3b-ft-cococap-448"),
      token_classification_ai=AIGenTokenClassificationBert(
        model_id="vblagoje/bert-english-uncased-finetuned-pos"
      ),
      reverse_geotagging=ReverseGeotagging(),
    )
    cls.strategy.init()

  @pytest.mark.asyncio
  async def test_calculate_image_keyword_list(self):
    image_path = f"{os.getcwd()}/src/tests/test_images/windmill_address_some_none.NEF"
    keyword_list = await self.strategy.calculate_image_keyword_list(
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
