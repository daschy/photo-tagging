from typing import List
import asyncio
from src.models.AIGenTokenClassificationBert import (
  TOKEN_TYPE,
  AIGenTokenClassificationBert,
)
from src.models.ReverseGeotagging import ReverseGeotagging
from src.models.AIGenPaliGemma import AIGenPaliGemma
from src.models.StrategyBase import StrategyBase


class StrategyCalculateKeywordList(StrategyBase):
  def __init__(
    self,
    image_to_text_ai: AIGenPaliGemma,
    token_classification_ai: AIGenTokenClassificationBert,
    reverse_geotagging: ReverseGeotagging,
  ):
    super().__init__()
    self.image_to_text_ai: AIGenPaliGemma = image_to_text_ai
    self.token_classification_ai: AIGenTokenClassificationBert = token_classification_ai
    self.reverse_geotagging: ReverseGeotagging = reverse_geotagging

  def init(self):
    self.image_to_text_ai.ai_init()
    self.token_classification_ai.ai_init()

  def _check_init(self):
    if self.image_to_text_ai.is_init() is False:
      raise ValueError("image_to_text_ai is not initialized")
    if self.token_classification_ai.is_init() is False:
      raise ValueError("token_classification_ai is not initialized")

  async def calculate_image_keyword_list(self, image_path: str) -> List[str]:
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
      output_keyword_list = sorted(list(set(token_list[0] + token_list[1] + token_list[2])))
      return output_keyword_list

    except FileNotFoundError as e:
      self.logger.exception(e)
      raise
    except Exception as e:
      self.logger.exception(e)
      raise
