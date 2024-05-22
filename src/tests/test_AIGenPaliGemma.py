import os
import pytest
from src.models.AIGenPaliGemma import AIGenPaliGemma


class TestAIGenPaliGemma:
  ai_gen = None

  @classmethod
  def setup_class(cls):
    cls.ai_gen = AIGenPaliGemma("google/paligemma-3b-ft-cococap-448")
    cls.ai_gen.ai_init()
    assert cls.ai_gen.model is not None
    assert cls.ai_gen.processor is not None

  @pytest.mark.asyncio
  async def test_generate(self):
    img_path = f"{os.getcwd()}/src/tests/test_images/person_biking_no_gps.NEF"
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
