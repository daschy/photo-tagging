import os
import pytest
import pytest_asyncio
from models.ReverseGeotagging import ReverseGeotagging
from models.ReverseGeotaggingXMP import ReverseGeotaggingXMP


@pytest_asyncio.fixture(scope="function")
def reverse_geotagging() -> ReverseGeotagging:
	return ReverseGeotaggingXMP()


@pytest.mark.asyncio
async def test_generate_reverse_geo_tags_image_with_no_gps(
	reverse_geotagging: ReverseGeotagging,
):
	# Call the generateReverseGeoTags function
	result = await reverse_geotagging.generate_reverse_geotag(
		f"{os.getcwd()}/tests/test_data/person_biking_no_gps.NEF"
	)

	# Verify the result
	assert result == []


# Verify the function was called with the correct arguments


@pytest.mark.asyncio
async def test_generate_reverse_geo_tags_image_with_gps_values(
	reverse_geotagging: ReverseGeotagging,
):
	# Call the generateReverseGeoTags function
	result = await reverse_geotagging.generate_reverse_geotag(
		f"{os.getcwd()}/tests/test_data/person_walking_gps.NEF"
	)

	# Verify the result
	assert result == ["Netherlands", "Amsterdam", "Nachtwachtlaan"]


@pytest.mark.asyncio
async def test_generate_reverse_geo_tags_image_with_some_address_none(
	reverse_geotagging: ReverseGeotagging,
):
	# Call the generateReverseGeoTags function
	result = await reverse_geotagging.generate_reverse_geotag(
		f"{os.getcwd()}/tests/test_data/windmill_address_some_none.NEF"
	)

	# Verify the result
	assert result == ["Netherlands", "Aalsmeer", "Meester Jac. Takkade"]
