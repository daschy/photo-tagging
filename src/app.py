from Utils.LoggerUtils import GetLogger
import asyncio
from typing import List
from ImageToText import generateCaptionTags
from ImageToReverseGeoTagging import generateReverseGeoTags
from Utils.Images import *


async def execute(image_path) -> List[str]:
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
    images = [
        people_park_smoking, #//ZDS_1759.NEF
        people_biking, #//ZDS_2610.NEF
        nature_dog, #//ZDS_2276.NEF
        nature_mushroom, #//ZDS_1780.NEF
        nature_woods, #//ZDS_2322.NEF
    ]
    keywords = await asyncio.gather(*([execute(img) for img in images]))
    for idx, image_path in enumerate(images):

        tagList = keywords[idx]
        log.info(f"{image_path}: {tagList}")


if __name__ == "__main__":
    log = GetLogger(__name__)
    asyncio.run(main())
