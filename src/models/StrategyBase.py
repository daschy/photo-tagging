from abc import ABC, abstractmethod
from typing import List


class StrategyBase(ABC):
  @abstractmethod
  async def generate_keyword_list_image(self, image_path: str) -> List[str]:
    pass
