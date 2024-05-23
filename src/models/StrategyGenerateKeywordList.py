import os
from glob import glob
from typing import List
import asyncio
from src.models.orm.CrudBase import CRUDBase
from src.models.orm.Photo import Photo
from src.models.AIGenTokenClassificationBert import (
  TOKEN_TYPE,
  AIGenTokenClassificationBert,
)
from src.models.ReverseGeotagging import ReverseGeotagging
from src.models.AIGenPaliGemma import AIGenPaliGemma
from src.models.StrategyBase import StrategyBase
from src.utils.db_utils_async import get_db_session, init_engine


class StrategyGenerateKeywordList(StrategyBase):
  def __init__(
    self,
    image_to_text_ai: AIGenPaliGemma,
    token_classification_ai: AIGenTokenClassificationBert,
    reverse_geotagging: ReverseGeotagging,
    db_path: str,
  ):
    super().__init__()
    self.image_to_text_ai: AIGenPaliGemma = image_to_text_ai
    self.token_classification_ai: AIGenTokenClassificationBert = token_classification_ai
    self.reverse_geotagging: ReverseGeotagging = reverse_geotagging
    self.db_path = db_path

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
      text = caption_color_list[0] + caption_color_list[1]
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

  async def save(self, image_path: str, keyword_list: List[str]) -> bool:
    try:
      session = get_db_session(self.db_engine)
      async with session() as db:
        photo_crud = CRUDBase(Photo)
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

  async def generate_keyword_list_directory(self, root_dir: str) -> bool:
    extensions = [".png", ".jpg", ".jpeg", ".tiff", ".nef", ".tiff"]
    # for subdir, _, file_name_list in os.walk(root_dir):
    # for idx, file_name in enumerate(file_name_list):
    file_name_list = []
    for ext in extensions:
      pattern = os.path.join(root_dir, "**", f"*{ext.lower()}")
      file_name_list += glob(
        pattern,
        recursive=True,
      )
      pattern = os.path.join(root_dir, "**", f"*{ext.upper()}")
      file_name_list += glob(
        pattern,
        recursive=True,
      )

    for idx, file_name in enumerate(file_name_list):
      ext = os.path.splitext(file_name)[-1].lower()
      if ext in extensions:
        image_path = file_name  # os.path.join(subdir, file_name)
        session = get_db_session(self.db_engine)
        async with session() as db:
          photo_crud = CRUDBase(Photo)
          retrieved_photo = await photo_crud.get_by(db, path=image_path)
        if retrieved_photo is None:
          keyword_list = await self.generate_keyword_list_image(image_path=image_path)
          self.logger.debug(f"{os.path.split(image_path)[1]}: {keyword_list}")
          await self.save(image_path=image_path, keyword_list=keyword_list)
      self.logger.debug(f"{idx+1}/{len(file_name_list)} end")
    return True
