import pytest
import pytest_asyncio

from models.orm.BaseOrm import BaseOrm
from models.ReverseGeotagging import ReverseGeotagging
from models.AIGenPipeline import AIGenPipeline
from models.AIGenPretrained import AIGenPretrained
from models.StrategyGenerateKeywordList import StrategyGenerateKeywordList


class TestPhotoTaggingProcessor:
	@pytest_asyncio.fixture(scope="function")
	# async def strategy(self):
	#   output = StrategyGenerateKeywordList(
	#     image_to_text_ai=AIGenPretrained(model_id="google/paligemma-3b-ft-cococap-448"),
	#     token_classification_ai=AIGenPipeline(
	#       model_id="vblagoje/bert-english-uncased-finetuned-pos"
	#     ),
	#     reverse_geotagging=ReverseGeotagging(),
	#     # db_path=f"sqlite+aiosqlite:////{self.test_db_path}",
	#   )
	#   await output.init()
	#   yield output
	#   async with output.db_engine.begin() as conn:
	#     await conn.run_sync(BaseOrm.metadata.drop_all)

	@pytest.mark.asyncio
	async def test_execute(self, strategy):
		# output =
		assert False


if __name__ == "__main__":
	pytest.main()
