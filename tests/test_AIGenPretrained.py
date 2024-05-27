import os
import pytest
from models.AIGen import AIGen
from models.AIGenPretrained import AIGenParamsPaliGemma, AIGenPretrained


class TestAIGenPretrained:
	ai_gen: AIGen[AIGenParamsPaliGemma]

	@classmethod
	def setup_class(cls):
		cls.ai_gen = AIGenPretrained("google/paligemma-3b-ft-cococap-448")
		cls.ai_gen.ai_init()
		assert cls.ai_gen.model is not None
		assert cls.ai_gen.processor is not None

	@pytest.mark.asyncio
	async def test_generate(self):
		file_path = f"{os.getcwd()}/tests/test_data/person_biking_no_gps.NEF"
		text = await self.ai_gen.generate(file_path=file_path, text="caption")
		assert text is not None
		try:
			text = await self.ai_gen.generate(file_path=file_path, text=None)
		except ValueError:
			assert True
		try:
			text = await self.ai_gen.generate(file_path=file_path, text="")
		except ValueError:
			assert True
