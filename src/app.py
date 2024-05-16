from Utils.LoggerUtils import GetLogger
import asyncio
from typing import List
from CaptionTagging import generateCaptionTags
from ReverseGeoTagging import generateReverseGeoTags
from Utils.Images import *


async def execute(image_path):
    featureTags: List[str] = await generateCaptionTags(
        image_path
    ) + await generateReverseGeoTags(image_path)

    outputTags: List[str] = list(set(featureTags))
    return outputTags


async def main():
    # image_path = "/Users/1q82/Pictures/Photos/Amsterdam/Nature/ZDS_1780.NEF"
    # image_path = "/Users/1q82/Pictures/Photos/Amsterdam/Nature/ZDS_0716.NEF"
    # image_path = "/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_2610.NEF"
    # image_path = "/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_1759.NEF"
    image_path = people_biking
    tagList = await execute(image_path)
    log.debug(f"{tagList}")


if __name__ == "__main__":
    log = GetLogger(__name__)
    asyncio.run(main())
