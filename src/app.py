import logging
import asyncio
from typing import List
from ImageCaptionGenerate import generateCaptionTags


# from ImageReverseGeoTagging import get_gps_coordinates, reverse_geotag
# from ImageKeywords import captionListToKeywords
# from ImageCaptionGenerate import generateCaptionList


# Example usage


# image_caption_list = generateCaptionList(image_path)
# keywords = captionListToKeywords([item.caption for item in image_caption_list])
# coordinates = get_gps_coordinates(image_path)
# if coordinates:
#     print("GPS Coordinates:", coordinates)
# else:
#     print("No GPS coordinates found in the image EXIF data.")

# latitude = coordinates[0]  # Example latitude
# longitude = coordinates[1]

# address = reverse_geotag(latitude, longitude)
# if address:
#     print(address)
# else:
#     pp("No address found for the provided coordinates.")


# pp([address.country, address.city, address.road] + keywords)


async def execute(image_path):
    captionTags: List[str] = await generateCaptionTags(image_path)
    geoTags: List[str] = []
    featureTags: List[str] = []
    return captionTags + geoTags + featureTags


async def main():
    image_path = "/Users/1q82/Pictures/Photos/Amsterdam/Nature/ZDS_1780.NEF"
    image_path = "/Users/1q82/Pictures/Photos/Amsterdam/Nature/ZDS_0716.NEF"
    image_path = "/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_2610.NEF"
    image_path = "/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_1759.NEF"
    tagList = await execute(image_path)
    for caption in tagList:
        log.debug(f"{caption}")


if __name__ == "__main__":
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    logging.basicConfig(
        format="%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s",
        # level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    asyncio.run(main())
