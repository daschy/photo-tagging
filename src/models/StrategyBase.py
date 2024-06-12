import os
from glob import glob
from abc import abstractmethod
from typing import List

from models.Base import Base
from models.orm.Photo import Photo


class StrategyBase(Base):
	def get_file_list(self, directory_path, extension_list, exclude_path_list):
		file_name_list: List[str] = []
		for ext in extension_list:
			pattern = os.path.join(directory_path, "**", f"*.{ext.lower()}")
			file_name_list += glob(
				pattern,
				recursive=True,
			)
			pattern = os.path.join(directory_path, "**", f"*.{ext.upper()}")
			file_name_list += glob(
				pattern,
				recursive=True,
			)
		if bool(exclude_path_list):
			ex_file_name_list = [
				path
				for path in file_name_list
				if not any(
					f"{exclude_path}".lower() in os.path.basename(os.path.dirname(path)).lower()
					for exclude_path in exclude_path_list
				)
			]
			file_name_list = ex_file_name_list
		return file_name_list

	@abstractmethod
	async def is_file_processed(self, photo: Photo) -> bool:
		pass

	@abstractmethod
	async def generate_keyword_list_image(self, image_path: str) -> List[str]:
		pass

	@abstractmethod
	async def generate_keyword_list_directory(
		self,
		directory_path: str,
		extension_list: List[str],
		exclude_path_list: List[str],
		save_on_file: bool,
	) -> bool:
		pass
