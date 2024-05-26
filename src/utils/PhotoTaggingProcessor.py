from src.models.Base import Base
from src.models.StrategyBase import StrategyBase


class PhotoTaggingProcessor(Base):
  strategy: StrategyBase

  def set_strategy(self, strategy: StrategyBase):
    self.strategy = strategy

  async def execute(self, directory_path: str):
    return self.strategy.generate_keyword_list_directory(
      directory_path=directory_path,
      extension_list=["png", "jpg", "jpeg", "tiff", "nef", "tiff"],
      save_on_db=True,
      save_on_file=True,
    )
