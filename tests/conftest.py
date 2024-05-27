import pytest

from models.AIGenPipeline import AIGenPipeline
from models.AIGenPretrained import AIGenPretrained
from models.ExifFileCRUD import ExifFileCRUD
from models.ReverseGeotagging import ReverseGeotagging
from models.StrategyGenerateKeywordList import StrategyGenerateKeywordList


@pytest.fixture(scope="module")
def exif_crud():
	output = ExifFileCRUD()
	yield output

@pytest.fixture(scope="module", autouse=True)
def strategy():
	output = StrategyGenerateKeywordList(
		image_to_text_ai=AIGenPretrained(model_id="google/paligemma-3b-ft-cococap-448"),
		token_classification_ai=AIGenPipeline(
			model_id="vblagoje/bert-english-uncased-finetuned-pos"
		),
		reverse_geotagging=ReverseGeotagging(),
	)
	# await output.init()
	yield output