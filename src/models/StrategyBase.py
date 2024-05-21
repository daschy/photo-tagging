from abc import ABC, abstractmethod
from typing import List


class StrategyBase(ABC):
  @abstractmethod
  async def save_keyword_list(self, image_path: str) -> List[str]:
    pass
