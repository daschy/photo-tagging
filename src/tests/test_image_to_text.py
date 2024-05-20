import os
import pytest
from src.utils.image_to_text import (
  generate_caption_keyword_list,
)


@pytest.mark.asyncio
async def test_generate_caption_keyword_list():
  result = await generate_caption_keyword_list(
    f"{os.getcwd()}/src/tests/test_images/person_biking_no_gps.NEF"
  )

  assert sorted(result) == sorted([
    "bag",
    "building",
    "bike",
    "sneakers",
    "black",
    "shorts",
    "kickstand",
    "blue",
    "brick sidewalk",
    "tire",
    "man",
    "window",
    "front",
  ])


# If this script is executed directly, run pytest
if __name__ == "__main__":
  pytest.main()
