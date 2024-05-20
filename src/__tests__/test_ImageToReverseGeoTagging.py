import pytest
from src.ImageToReverseGeoTagging import (
  generate_reverse_geo_tags,
)


@pytest.mark.asyncio
async def TestGenerateReverseGeoTagsNoGps():
  # Call the generateReverseGeoTags function
  result = await generate_reverse_geo_tags(
    "/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_2610.NEF"
  )

  # Verify the result
  assert result == []

  # Verify the function was called with the correct arguments


@pytest.mark.asyncio
async def TestGenerateReverseGeoTagsGpsValues():
  # Call the generateReverseGeoTags function
  result = await generate_reverse_geo_tags(
    "/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_1759.NEF"
  )

  # Verify the result
  assert result == ["Netherlands", "Amsterdam", "Vondelpark"]


# If this script is executed directly, run pytest
if __name__ == "__main__":
  pytest.main()
