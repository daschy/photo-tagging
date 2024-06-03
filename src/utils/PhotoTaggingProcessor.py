from models.Base import Base
from models.StrategyBase import StrategyBase


class PhotoTaggingProcessor(Base):
	strategy: StrategyBase

	def set_strategy(self, strategy: StrategyBase) -> "PhotoTaggingProcessor":
		self.strategy = strategy
		return self

	async def execute(self, directory_path: str, dry_run: bool = True) -> bool:
		return await self.strategy.generate_keyword_list_directory(
			directory_path=directory_path,
			extension_list=["nef", "jpg", "jpeg"],
			save_on_file=not dry_run,
		)
