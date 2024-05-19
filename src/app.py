from Logger.LoggerUtils import GetLogger
import asyncio
from typing import List
from ImageToText import generateCaptionTags
from ImageToReverseGeoTagging import generateReverseGeoTags
from Utils import Images
from Models.Photo import Photo
from Utils.DbUtils import init_db, AsyncSessionLocal
from Models.CrudBase import CRUDBase



async def execute(db, image_path) -> List[str]:
    featureKeywordList: List[List[str]] = await asyncio.gather(
        generateCaptionTags(image_path), generateReverseGeoTags(image_path)
    )
    outputKeywordList: List[str] = list(
        set(featureKeywordList[0] + featureKeywordList[1])
    )
    photo_crud = CRUDBase(Photo)
    retrievedPhoto = await photo_crud.get_by(db, path=image_path)
    if retrievedPhoto is None:
        newPhoto = Photo(image_path)
        newPhoto.addKeywordList(outputKeywordList)
        await photo_crud.create(db, newPhoto)
    else:
        retrievedPhoto.setKeywordList(outputKeywordList)
        await photo_crud.update(db, retrievedPhoto.id, retrievedPhoto)
    return outputKeywordList


async def main():
    images = [
        Images.people_park_smoking,  # //ZDS_1759.NEF
        # Images.people_biking,  # //ZDS_2610.NEF
        # Images.nature_flower,  # //ZDS_1788.NEF
        # Images.nature_dog,  # //ZDS_2276.NEF
        # Images.nature_mushroom,  # //ZDS_1780.NEF
        # Images.nature_woods,  # //ZDS_2322.NEF
    ]
    await init_db()
    async with AsyncSessionLocal() as db:
        keywords = await asyncio.gather(*([execute(db, img) for img in images]))

        for idx, image_path in enumerate(images):
            tagList = keywords[idx]
            log.info(f"{image_path}: {tagList}")


if __name__ == "__main__":
    log = GetLogger(__name__)
    asyncio.run(main())
