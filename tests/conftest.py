from collections.abc import Generator
import pytest
from mock import patch, PropertyMock
from pytest_mock import MockerFixture
from models.AIGen import AIGen
from models.AIGenBert import TOKEN_TYPE, AIGenBert
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
	return output


@pytest.fixture(scope="module")
def test_keyword_list_colors():
	output = [
		"black",
		"blue",
		"white",
	]
	return output


@pytest.fixture(scope="module")
def test_keyword_list_address():
	output = [
		"Aalsmeer",
		"Meester Jac. Takkade",
		"Netherlands",
	]
	return output


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


@pytest.fixture(scope="module")
def strategy_gen_keyword_list(
	module_mocker: MockerFixture,
	test_keyword_list_caption: list[str],
	test_keyword_list_colors: list[str],
	mock_reverse_geotaggin_xml: ReverseGeotagging,
	mock_db_crud_photo: DBCRUD[Photo],
	mock_db_exif_file_crud: ExifFileCRUD,
):
	module_mocker.patch.object(
		AIGenPaliGemma,
		"is_init",
		return_value=True,
	)
	module_mocker.patch.object(
		AIGenPaliGemma,
		"ai_init",
		return_value=None,
	)

	module_mocker.patch.object(
		AIGenPaliGemma,
		"_generate_text",
		side_effect=lambda file_path, prompt: (
			"A windmill with a blue sky in the background."
			if prompt == "caption"
			else "blue,white and black"
		),
	)

	mock_ai_paligemma_caption = AIGenPaliGemma(
		model_id="google/paligemma-3b-ft-cococap-448",
		prompt="caption",
	)

	mock_ai_paligemma_colors = AIGenPaliGemma(
		model_id="google/paligemma-3b-ft-cococap-448",
		prompt="colors",
	)

	module_mocker.patch.object(
		AIGenPaliGemma,
		"is_init",
		return_value=True,
	)
	module_mocker.patch.object(
		AIGenPaliGemma,
		"ai_init",
		return_value=None,
	)

	module_mocker.patch.object(
		AIGenPaliGemma,
		"_generate_text",
		side_effect=lambda file_path, prompt: (
			"A windmill with a blue sky in the background."
			if prompt == "caption"
			else "blue,white and black"
		),
	)

	mock_ai_paligemma_colors = AIGenPaliGemma(
		model_id="google/paligemma-3b-ft-cococap-448",
		prompt="colors",
	)

	module_mocker.patch.object(
		AIGenBert,
		"is_init",
		return_value=True,
	)
	module_mocker.patch.object(
		AIGenBert,
		"ai_init",
		return_value=None,
	)

	module_mocker.patch.object(
		AIGenBert,
		"generate",
		side_effect=lambda token_type, text: (
			test_keyword_list_caption
			if token_type == TOKEN_TYPE.NOUN
			else test_keyword_list_colors
		),
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
