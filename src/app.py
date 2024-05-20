import asyncio
from typing import List

from ImageToText import generate_caption_tags
from ImageToReverseGeoTagging import generate_reverse_geo_tags
from Logger.logger_utils import get_logger
from Models.Photo import Photo
from Models.CrudBase import CRUDBase
from utils import Images
from utils.DbUtils import init_db, AsyncSessionLocal


log = get_logger(__name__)


async def execute(db, image_path) -> List[str]:
  photo_crud = CRUDBase(Photo)
  retrieved_photo = await photo_crud.get_by(db, path=image_path)
  image_keyword_list = []
  if retrieved_photo is None:
    feature_keyword_list: List[List[str]] = await asyncio.gather(
      generate_caption_tags(image_path), generate_reverse_geo_tags(image_path)
    )
    image_keyword_list: List[str] = list(
      set(feature_keyword_list[0] + feature_keyword_list[1])
    )
    new_photo = Photo(image_path)
    new_photo.addKeywordList(image_keyword_list)
    await photo_crud.create(db, new_photo)
  else:
    image_keyword_list = retrieved_photo.keywordList
  return image_keyword_list


async def main():
  image_paths = [
    Images.people_park_smoking,  # //ZDS_1759.NEF
    Images.people_biking,  # //ZDS_2610.NEF
    Images.nature_flower,  # //ZDS_1788.NEF
    Images.nature_dog,  # //ZDS_2276.NEF
    Images.nature_mushroom,  # //ZDS_1780.NEF
    Images.nature_woods,  # //ZDS_2322.NEF
  ]
  await init_db()
  async with AsyncSessionLocal() as db:
    photo_crud = CRUDBase(Photo)
    keyword_list = []
    for idx, image_path in enumerate(image_paths):
      retrieved_photo = await photo_crud.get_by(db, path=image_path)
      if retrieved_photo is None:
        photo_crud = CRUDBase(Photo)
        keyword_list = await asyncio.gather(
          *([execute(db, img) for img in image_paths])
        )
      else:
        keyword_list.append(retrieved_photo.keywordList)

    for idx, image_path in enumerate(image_paths):
      tag_list = keyword_list[idx]
      log.info(f"{image_path}: {tag_list}")


if __name__ == "__main__":
  log = get_logger(__name__)
  asyncio.run(main())
