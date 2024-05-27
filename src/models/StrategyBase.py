from abc import abstractmethod
from typing import List

from models.Base import Base


class StrategyBase(Base):
	@abstractmethod
	async def generate_keyword_list_image(self, image_path: str) -> List[str]:
		pass

	@abstractmethod
	async def generate_keyword_list_directory(
		self,
		directory_path: str,
		extension_list: List[str],
		save_on_file: bool,
		save_on_db: bool,
	) -> bool:
		pass
