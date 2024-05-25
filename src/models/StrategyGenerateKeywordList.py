import asyncio
import os
from glob import glob
from typing import List

from src.models.AIGenPretrained import AIGenPretrained
from src.models.AIGenPipeline import TOKEN_TYPE, AIGenPipeline
from src.models.ImageCRUD import ImageCRUD
from src.models.DBCRUD import DBCRUD
from src.models.orm.Photo import Photo
from src.models.ReverseGeotagging import ReverseGeotagging
from src.models.StrategyBase import StrategyBase
from src.utils.db_utils_async import get_db_session, init_engine


class StrategyGenerateKeywordList(StrategyBase):
  def __init__(
    self,
    image_to_text_ai: AIGenPretrained,
    token_classification_ai: AIGenPipeline,
    reverse_geotagging: ReverseGeotagging,
    db_path: str,
  ):
    super().__init__()
    self.image_to_text_ai: AIGenPretrained = image_to_text_ai
    self.token_classification_ai: AIGenPipeline = token_classification_ai
    self.reverse_geotagging: ReverseGeotagging = reverse_geotagging
    self.db_path = db_path
    self.image_crud = ImageCRUD()

  async def init(self):
    self.image_to_text_ai.ai_init()
    self.token_classification_ai.ai_init()
    self.db_engine = await init_engine(self.db_path)

  def _check_init(self):
    if self.image_to_text_ai.is_init() is False:
      raise ValueError("image_to_text_ai is not initialized")
    if self.token_classification_ai.is_init() is False:
      raise ValueError("token_classification_ai is not initialized")

  async def generate_keyword_list_image(self, image_path: str) -> List[str]:
    try:
      self._check_init()
      output_keyword_list = []
      caption_color_list: List[str] = await asyncio.gather(
        self.image_to_text_ai.generate_text(img_path=image_path, prompt="caption"),
        self.image_to_text_ai.generate_text(
          img_path=image_path,
          prompt="what are the four most dominant colors in the picture?",
        ),
      )
      text = caption_color_list[0] + " " + caption_color_list[1]
      token_list: List[List[str]] = await asyncio.gather(
        self.token_classification_ai.generate_token_list(
          text=text, token_type=TOKEN_TYPE.NOUN
        ),
        self.token_classification_ai.generate_token_list(
          text=text, token_type=TOKEN_TYPE.ADJ
        ),
        self.reverse_geotagging.generate_reverse_geotag(image_path=image_path),
      )
      output_keyword_list = sorted(
        list(set(token_list[0] + token_list[1] + token_list[2])), key=str.casefold
      )
      return output_keyword_list

    except FileNotFoundError as e:
      self.logger.exception(e)
      raise
    except Exception as e:
      self.logger.exception(e)
      raise

  async def save_to_file(self, image_path: str, keyword_list: List[str]) -> bool:
    output = await self.image_crud.save_keyword_list(
      image_path, keyword_list=keyword_list
    )
    return output

  async def save_to_db(self, image_path: str, keyword_list: List[str]) -> bool:
    try:
      session = get_db_session(self.db_engine)
      async with session() as db:
        photo_crud = DBCRUD(Photo)
        new_photo = Photo(image_path)
        new_photo.set_keyword_list(keyword_list)
        await photo_crud.create(db, new_photo)
      return True

    except FileNotFoundError as e:
      self.logger.exception(e, f"Failed to add keywords to {image_path}: {e}")
      raise
    except Exception as e:
      self.logger.exception(e, f"Failed to add keywords to {image_path}: {e}")
      raise

  async def generate_keyword_list_directory(
    self,
    root_dir: str,
    extension_list: List[str] = [],
    save_on_file: bool = False,
    save_on_db: bool = True,
  ) -> bool:
    extension_list_ = (
      extension_list
      if len(extension_list) > 0
      else ["png", "jpg", "jpeg", "tiff", "nef", "tiff"]
    )
    file_name_list = []
    for ext in extension_list_:
      pattern = os.path.join(root_dir, "**", f"*.{ext.lower()}")
      file_name_list += glob(
        pattern,
        recursive=True,
      )
      pattern = os.path.join(root_dir, "**", f"*.{ext.upper()}")
      file_name_list += glob(
        pattern,
        recursive=True,
      )

    for idx, file_name in enumerate(file_name_list):
      ext = os.path.splitext(file_name)[-1].lower()
      image_path = file_name  # os.path.join(subdir, file_name)
      session = get_db_session(self.db_engine)
      async with session() as db:
        photo_crud = DBCRUD(Photo)
        retrieved_photo = await photo_crud.get_by(db, path=image_path)
      if retrieved_photo is None:
        keyword_list = await self.generate_keyword_list_image(image_path=image_path)
        self.logger.info(f"{os.path.split(image_path)[1]}: {keyword_list}")
        if save_on_db:
          await self.save_to_db(image_path=image_path, keyword_list=keyword_list)
        if save_on_file:
          await self.save_to_file(image_path=image_path, keyword_list=keyword_list)
      self.logger.info(f"{idx+1}/{len(file_name_list)} end")
    return True
