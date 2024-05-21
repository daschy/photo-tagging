from src.models.StrategyBase import StrategyBase


class PhotoKeywordContext:
  def __init__(self, strategy: StrategyBase):
    self._strategy = strategy

  def set_strategy(self, strategy: StrategyBase):
    self._strategy = strategy

  async def add_keywords(self, image_path):
    await self._strategy.save_keyword_list(image_path)
