from Utils.LoggerUtils import GetLogger
import asyncio
from typing import List
from ImageToText import generateCaptionTags
from ImageToReverseGeoTagging import generateReverseGeoTags
from Utils import Images


async def execute(image_path) -> List[str]:
    featureTags: List[List[str]] = await asyncio.gather(
        generateCaptionTags(image_path), generateReverseGeoTags(image_path)
    )

    outputTags: List[str] = list(set(featureTags[0] + featureTags[1]))
    return outputTags


async def main():
    images = [
        Images.people_park_smoking,  # //ZDS_1759.NEF
        Images.people_biking,  # //ZDS_2610.NEF
        Images.nature_flower,  # //ZDS_1788.NEF
        Images.nature_dog,  # //ZDS_2276.NEF
        Images.nature_mushroom,  # //ZDS_1780.NEF
        Images.nature_woods,  # //ZDS_2322.NEF
    ]
    keywords = await asyncio.gather(*([execute(img) for img in images]))
    for idx, image_path in enumerate(images):
        tagList = keywords[idx]
        log.info(f"{image_path}: {tagList}")


if __name__ == "__main__":
    log = GetLogger(__name__)
    asyncio.run(main())
