import os
import pytest
from src.models.AIGenPretrained import AIGenPretrained


class TestAIGenPretrained:
  ai_gen = None

  @classmethod
  def setup_class(cls):
    cls.ai_gen = AIGenPretrained("google/paligemma-3b-ft-cococap-448")
    cls.ai_gen.ai_init()
    assert cls.ai_gen.model is not None
    assert cls.ai_gen.processor is not None

  @pytest.mark.asyncio
  async def test_generate(self):
    img_path = f"{os.getcwd()}/tests/test_data/person_biking_no_gps.NEF"
    text = await self.ai_gen.generate_text(img_path, "caption")
    assert text is not None
    try:
      text = await self.ai_gen.generate_text(img_path, None)
    except ValueError:
      assert True
    try:
      text = await self.ai_gen.generate_text(img_path, "")
    except ValueError:
      assert True
