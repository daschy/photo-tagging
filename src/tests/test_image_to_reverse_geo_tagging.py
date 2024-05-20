import os
import pytest
from src.utils.image_to_reverse_geo_tagging import (
  generate_reverse_geo_tags,
)


@pytest.mark.asyncio
async def test_GenerateReverseGeoTagsNoGps():
  # Call the generateReverseGeoTags function 
  result = await generate_reverse_geo_tags(f"{os.getcwd()}/src/tests/test_images/person_biking_no_gps.NEF")

  # Verify the result
  assert result == []

  # Verify the function was called with the correct arguments


@pytest.mark.asyncio
async def test_GenerateReverseGeoTagsGpsValues():
  # Call the generateReverseGeoTags function
  result = await generate_reverse_geo_tags(f"{os.getcwd()}/src/tests/test_images/person_walking_gps.NEF")

  # Verify the result
  assert result == ["Netherlands", "Amsterdam", "Nachtwachtlaan"]


# If this script is executed directly, run pytest
if __name__ == "__main__":
  pytest.main()
