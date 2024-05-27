import os
import pytest
import pytest_asyncio

from models.ReverseGeotagging import ReverseGeotagging
from models.ReverseGeotaggingXMP import ReverseGeotaggingXMP
from tests.test_ReverseGeotagging import TestReverseGeotagging


class TestReverseGeotaggingXMP:
	@pytest_asyncio.fixture(scope="function")
	def reverse_geotagging(self) -> ReverseGeotagging:
		return ReverseGeotaggingXMP()

	@pytest.mark.asyncio
	async def test_generate_reverse_geo_tags_image_with_no_gps_and_xmp(
		self,
		reverse_geotagging: ReverseGeotagging,
	):
		# Call the generateReverseGeoTags function
		result = await reverse_geotagging.generate_reverse_geotag(
			f"{os.getcwd()}/tests/test_data/image_with_no_gps_with_xmp.NEF"
		)

		# Verify the result
		assert result == ["Netherlands", "Amsterdam", "Prins Hendrikkade"]

		# Verify the function was called with the correct arguments

	@pytest.mark.asyncio
	async def test_generate_reverse_geo_tags_image_with_gps_values_and_no_xmp_file(
		self,
		reverse_geotagging: ReverseGeotagging,
	):
		# Call the generateReverseGeoTags function
		result = await reverse_geotagging.generate_reverse_geotag(
			f"{os.getcwd()}/tests/test_data/person_walking_gps.NEF"
		)

		# Verify the result
		assert result == ["Netherlands", "Amsterdam", "Nachtwachtlaan"]
