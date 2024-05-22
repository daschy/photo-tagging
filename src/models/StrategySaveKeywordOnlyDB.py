from logging import Logger
from typing import List
import asyncio
from sqlalchemy.orm import sessionmaker
from src.models.CrudBase import CRUDBase
from src.models.Photo import Photo
from src.models.StrategyBase import StrategyBase
from src.utils.image_to_reverse_geo_tagging import generate_reverse_geotag
from src.utils.image_to_keyword_list import generate_keyword_list


class StrategySaveKeywordOnlyDB(StrategyBase):
  def __init__(self, logger: Logger, db: sessionmaker):
    self.db = db
    self.logger = logger

  async def save_keyword_list(self, image_path: str) -> None:
    try:
      photo_crud = CRUDBase(Photo)
      retrieved_photo = await photo_crud.get_by(self.db, path=image_path)
      image_keyword_list = []
      if retrieved_photo is None:
        feature_keyword_list: List[List[str]] = await asyncio.gather(
          generate_keyword_list(image_path), generate_reverse_geotag(image_path)
        )
        image_keyword_list: List[str] = sorted(
          list(set(feature_keyword_list[0] + feature_keyword_list[1]))
        )
        new_photo = Photo(image_path)
        new_photo.add_keyword_list(image_keyword_list)
        await photo_crud.create(self.db, new_photo)
      else:
        image_keyword_list = retrieved_photo.keyword_list
      return image_keyword_list

    except FileNotFoundError as e:
      self.logger.exception(e, f"Failed to add keywords to {image_path}: {e}")
      raise
    except Exception as e:
      self.logger.exception(e, f"Failed to add keywords to {image_path}: {e}")
      raise
