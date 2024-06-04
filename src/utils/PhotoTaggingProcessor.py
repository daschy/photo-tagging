from typing import List
from models.Base import Base
from models.StrategyBase import StrategyBase


class PhotoTaggingProcessor(Base):
	strategy: StrategyBase

	def set_strategy(self, strategy: StrategyBase) -> "PhotoTaggingProcessor":
		self.strategy = strategy
		return self

	async def execute(
		self, directory_path: str, exclude_dir_list: List[str] = [], dry_run: bool = True
	) -> bool:
		return await self.strategy.generate_keyword_list_directory(
			directory_path=directory_path,
			extension_list=["nef", "jpg", "jpeg"],
			exclude_path_list=exclude_dir_list,
			save_on_file=not dry_run,
		)
