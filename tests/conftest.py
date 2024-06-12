from collections.abc import Generator
import pytest

from pytest_mock import MockerFixture
from models.AIGenBert import AIGenBert
from models.AIGenPaliGemma import AIGenPaliGemma
from models.DBCRUD import DBCRUD
from models.ExifFileCRUD import ExifFileCRUD
from models.ReverseGeotagging import ReverseGeotagging
from models.ReverseGeotaggingXMP import ReverseGeotaggingXMP
from models.StrategyGenerateKeywordList import StrategyGenerateKeywordList
from models.orm.Photo import Photo


@pytest.fixture(scope="module")
def test_keyword_list_caption():
	output = [
		"background",
		"sky",
		"windmill",
	]
	yield output


@pytest.fixture(scope="module")
def test_keyword_list_colors():
	output = [
		"black",
		"blue",
		"white",
	]
	yield output


@pytest.fixture(scope="module")
def test_keyword_list_address():
	output = [
		"Aalsmeer",
		"Meester Jac. Takkade",
		"Netherlands",
	]
	yield output


@pytest.fixture(scope="module")
def test_keyword_list(
	test_keyword_list_caption: list[str],
	test_keyword_list_colors: list[str],
	test_keyword_list_address: list[str],
):
	output = sorted(
		list(
			set(
				test_keyword_list_caption + test_keyword_list_colors + test_keyword_list_address
			)
		),
		key=str.casefold,
	)
	yield output


@pytest.fixture(scope="module")
def exif_crud():
	exif_file_crud = ExifFileCRUD()
	yield exif_file_crud


@pytest.fixture(scope="module")
def mock_reverse_geotaggin_xml(
	module_mocker: MockerFixture,
	test_keyword_list_address: list[str],
) -> Generator[ReverseGeotaggingXMP, None, None]:
	mock_output = ReverseGeotaggingXMP()
	module_mocker.patch.object(
		mock_output,
		"generate_reverse_geotag",
		return_value=test_keyword_list_address,
	)
	yield mock_output


@pytest.fixture(scope="module")
def mock_db_crud_photo(
	module_mocker: MockerFixture,
):
	mock_output = DBCRUD[Photo](Photo)
	yield mock_output


@pytest.fixture(scope="module")
def mock_db_exif_file_crud(
	module_mocker: MockerFixture,
):
	mock_output = ExifFileCRUD()
	yield mock_output


@pytest.fixture(scope="module", autouse=True)
def strategy_gen_keyword_list(
	module_mocker: MockerFixture,
	mock_reverse_geotaggin_xml: ReverseGeotagging,
	mock_db_crud_photo: DBCRUD[Photo],
	mock_db_exif_file_crud: ExifFileCRUD,
):
	mock_ai_paligemma_caption = AIGenPaliGemma(
		model_id="google/paligemma-3b-ft-cococap-448",
		prompt="caption",
	)
	module_mocker.patch.object(
		mock_ai_paligemma_caption,
		"generate",
		return_value="A windmill with a blue sky in the background.",
	)
	mock_ai_paligemma_colors = AIGenPaliGemma(
		model_id="google/paligemma-3b-ft-cococap-448",
		prompt="what are the four most dominant colors in the picture?",
	)
	module_mocker.patch.object(
		mock_ai_paligemma_colors,
		"generate",
		return_value="blue,white and black",
	)

	mock_token_classificator = AIGenBert(
		model_id="vblagoje/bert-english-uncased-finetuned-pos",
	)

	output = StrategyGenerateKeywordList(
		image_to_text_ai_list=[
			mock_ai_paligemma_caption,
			mock_ai_paligemma_colors,
		],
		token_classification_ai=mock_token_classificator,
		reverse_geotagging=mock_reverse_geotaggin_xml,
		db_crud=mock_db_crud_photo,
		exif_crud=mock_db_exif_file_crud,
	)
	yield output
