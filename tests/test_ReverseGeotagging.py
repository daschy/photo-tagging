import os
import pytest
from models.ReverseGeotagging import ReverseGeotagging


class TestReverseGeotagging:
	reverse_geotagging: ReverseGeotagging = None

	@classmethod
	def setup_class(cls):
		assert True
		cls.reverse_geotagging = ReverseGeotagging()
		assert cls.reverse_geotagging is not None

	@pytest.mark.asyncio
	async def test_generate_reverse_geo_tags_image_with_no_gps(self):
		# Call the generateReverseGeoTags function
		result = await self.reverse_geotagging.generate_reverse_geotag(
			f"{os.getcwd()}/tests/test_data/person_biking_no_gps.NEF"
		)

		# Verify the result
		assert result == []

		# Verify the function was called with the correct arguments

	@pytest.mark.asyncio
	async def test_generate_reverse_geo_tags_image_with_gps_values(self):
		# Call the generateReverseGeoTags function
		result = await self.reverse_geotagging.generate_reverse_geotag(
			f"{os.getcwd()}/tests/test_data/person_walking_gps.NEF"
		)

		# Verify the result
		assert result == ["Netherlands", "Amsterdam", "Nachtwachtlaan"]

	@pytest.mark.asyncio
	async def test_generate_reverse_geo_tags_image_with_some_address_none(self):
		# Call the generateReverseGeoTags function
		result = await self.reverse_geotagging.generate_reverse_geotag(
			f"{os.getcwd()}/tests/test_data/windmill_address_some_none.NEF"
		)

		# Verify the result
		assert result == ["Netherlands", "Meester Jac. Takkade"]
