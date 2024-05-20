import pytest
from src.utils.image_to_reverse_geo_tagging import (
  generate_reverse_geo_tags,
)


@pytest.mark.asyncio
async def TestGenerateReverseGeoTagsNoGps():
  # Call the generateReverseGeoTags function
  result = await generate_reverse_geo_tags(
    "./src/__tests__/test_images/person_walking_gps.NEF"
  )

  # Verify the result
  assert result == []

  # Verify the function was called with the correct arguments


@pytest.mark.asyncio
async def TestGenerateReverseGeoTagsGpsValues():
  # Call the generateReverseGeoTags function
  result = await generate_reverse_geo_tags(
    "./src/__tests__/test_images/person_biking_no_gps.NEF"
  )

  # Verify the result
  assert result == ["Netherlands", "Amsterdam", "Vondelpark"]


# If this script is executed directly, run pytest
if __name__ == "__main__":
  pytest.main()
