from typing import List
from models.StrategyBase import StrategyBase


class StrategySaveInfoToFileFromSidecarDop(StrategyBase):
	async def generate_keyword_list_image(self, image_path: str) -> List[str]:
		raise NotImplementedError

	async def generate_keyword_list_directory(
		self,
		directory_path: str,
		extension_list: List[str],
		exclude_path_list: List[str],
		save_on_file: bool,
	) -> bool:
		raise NotImplementedError
