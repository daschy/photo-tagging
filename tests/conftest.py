import pytest

from models.AIGenBert import AIGenBert
from models.AIGenPaliGemma import AIGenPaliGemma
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
		image_to_text_ai_list=[
			AIGenPaliGemma(
				model_id="google/paligemma-3b-ft-cococap-448",
				prompt="caption",
			),
			AIGenPaliGemma(
				model_id="google/paligemma-3b-ft-cococap-448",
				prompt="what are the four most dominant colors in the picture?",
			),
		],
		token_classification_ai=AIGenBert(
			model_id="vblagoje/bert-english-uncased-finetuned-pos"
		),
		reverse_geotagging=ReverseGeotagging(),
	)
	# await output.init()
	yield output
