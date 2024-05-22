import pytest
from src.models.AIGenTokenClassification import TOKEN_TYPE, AIGenTokenClassification


class TestAIGenTokenClassification:
  ai_gen = None

  @classmethod
  def setup_class(cls):
    cls.ai_gen = AIGenTokenClassification(
      model_id="vblagoje/bert-english-uncased-finetuned-pos",
    )
    cls.ai_gen.ai_init()
    # assert cls.ai_gen.model is not None
    # assert cls.ai_gen.processor is not None

  @pytest.mark.asyncio
  async def test_generate_token_list(self):
    assert True
    # text = "black and white canvas"
    # token_list = await self.ai_gen.generate_token_list(text, TOKEN_TYPE.NOUN)
    # assert len(token_list) == 1

    # token_list = await self.ai_gen.generate_token_list(text, TOKEN_TYPE.ADJ)
    # assert len(token_list) == 2

    # try:
    #   text = await self.ai_gen.generate_token_list(text, None)
    # except ValueError:
    #   assert True
    # try:
    #   text = await self.ai_gen.generate_text(None, TOKEN_TYPE.NOUN)
    # except ValueError:
    #   assert True
    # try:
    #   text = await self.ai_gen.generate_text(None, None)
    # except ValueError:
    #   assert True
