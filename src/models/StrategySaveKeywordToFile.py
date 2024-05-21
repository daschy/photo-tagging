from logging import Logger
from typing import List

from src.models.StrategyBase import StrategyBase


class StrategySaveKeywordToFile(StrategyBase):
  def __init__(self, logger: Logger):
    self.logger = logger

  async def save_keyword_list(self, image_path: str) -> List[str]:
    return []
