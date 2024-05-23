from abc import abstractmethod
from typing import List

from src.models.Base import Base


class StrategyBase(Base):
  def __init__(self):
    super().__init__()

  @abstractmethod
  async def generate_keyword_list_image(self, image_path: str) -> List[str]:
    pass
