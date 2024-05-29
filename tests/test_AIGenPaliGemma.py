import os
import pytest
from models.AIGenPaliGemma import AIGenPaliGemma


class TestAIGenPaliGemma:
	@pytest.fixture(scope="function")
	def file_path(self):
		output = os.path.join(os.getcwd(), "tests", "test_data", "person_biking_no_gps.NEF")
		yield output

	@pytest.mark.asyncio
	async def test_generate(self, file_path):
		ai_gen = AIGenPaliGemma("google/paligemma-3b-ft-cococap-448", prompt="caption").ai_init()
		text = await ai_gen.generate(file_path=file_path)
		assert text is not None

	@pytest.mark.asyncio
	async def test_generate_prompt_is_falsy(self, file_path):
		with pytest.raises(ValueError):
			ai_gen = AIGenPaliGemma("google/paligemma-3b-ft-cococap-448", prompt="").ai_init()
			await ai_gen.generate(file_path=file_path)
