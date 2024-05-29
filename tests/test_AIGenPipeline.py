import pytest
from models.AIGen import AIGen
from models.AIGenBert import (
	TOKEN_TYPE,
	AIGenParamsBert,
	AIGenBert,
)


class TestAIGenPipeline:
	ai_gen: AIGen[AIGenParamsBert]

	@classmethod
	def setup_class(cls):
		assert True
		cls.ai_gen: AIGen[AIGenParamsBert] = AIGenBert(
			model_id="vblagoje/bert-english-uncased-finetuned-pos",
		)
		cls.ai_gen.ai_init()
		assert cls.ai_gen.model is not None
		assert cls.ai_gen.processor is not None

	@pytest.mark.asyncio
	async def test_generate(self):
		text = "black and white canvas"
		token_list = await self.ai_gen.generate(text=text, token_type=TOKEN_TYPE.NOUN)
		assert len(token_list) == 1

		token_list = await self.ai_gen.generate(text=text, token_type=TOKEN_TYPE.ADJ)
		assert len(token_list) == 2

		try:
			text = await self.ai_gen.generate(text=text, token_type=None)
		except ValueError:
			assert True
		try:
			text = await self.ai_gen.generate(text="", token_type=TOKEN_TYPE.NOUN)
		except ValueError:
			assert True
		try:
			text = await self.ai_gen.generate(text=None, token_type=None)
		except ValueError:
			assert True
