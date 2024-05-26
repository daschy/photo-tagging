import asyncio
import os
from glob import glob
from typing import List
import itertools
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from models.orm.Photo import Photo
from models.AIGenPretrained import AIGenPretrained
from models.AIGenPipeline import TOKEN_TYPE, AIGenPipeline
from models.ImageCRUD import ImageCRUD
from models.DBCRUD import DBCRUD

from models.ReverseGeotagging import ReverseGeotagging
from models.StrategyBase import StrategyBase
from utils.db_utils_async import get_db_session, init_engine


KEYWORD_LIST_DB_FILE_NAME: str = "keyword_list.db"


class StrategyGenerateKeywordList(StrategyBase):
	def __init__(
		self,
		image_to_text_ai: AIGenPretrained,
		token_classification_ai: AIGenPipeline,
		reverse_geotagging: ReverseGeotagging,
	):
		super().__init__()
		self.image_to_text_ai: AIGenPretrained = image_to_text_ai
		self.image_to_text_ai.ai_init()
		self.token_classification_ai: AIGenPipeline = token_classification_ai
		self.token_classification_ai.ai_init()
		self.reverse_geotagging: ReverseGeotagging = reverse_geotagging
		self.image_crud = ImageCRUD()

	def _check_init(self):
		if self.image_to_text_ai.is_init() is False:
			raise ValueError("image_to_text_ai is not initialized")
		if self.token_classification_ai.is_init() is False:
			raise ValueError("token_classification_ai is not initialized")

	async def generate_keyword_list_image(self, image_path: str) -> List[str]:
		try:
			self._check_init()
			caption_color_list: List[str] = list(
				await asyncio.gather(
					self.image_to_text_ai.generate_text(img_path=image_path, prompt="caption"),
					self.image_to_text_ai.generate_text(
						img_path=image_path,
						prompt="what are the four most dominant colors in the picture?",
					),
				)
			)
			text = " ".join(caption_color_list)
			token_list: List[List[str]] = list(
				await asyncio.gather(
					self.token_classification_ai.generate_token_list(
						text=text, token_type=TOKEN_TYPE.NOUN
					),
					self.reverse_geotagging.generate_reverse_geotag(image_path=image_path),
					self.token_classification_ai.generate_token_list(
						text=text, token_type=TOKEN_TYPE.ADJ
					),
				)
			)
			output_keyword_list: List[str] = sorted(
				list(set(itertools.chain.from_iterable(token_list))), key=str.casefold
			)
			return output_keyword_list

		except FileNotFoundError as e:
			self.logger.exception(e)
			raise
		except Exception as e:
			self.logger.exception(e)
			raise

	async def save_to_file(self, file_path: str, keyword_list: List[str]) -> bool:
		output = await self.image_crud.save_keyword_list(
			file_path, keyword_list=keyword_list
		)
		return output

	async def save_to_db(
		self, db: AsyncSession, image_path: str, keyword_list: List[str]
	) -> bool:
		try:
			photo_crud = DBCRUD(Photo)
			new_photo = Photo(image_path)
			new_photo.set_keyword_list(keyword_list)
			await photo_crud.create(db, new_photo)
			return True
		except FileNotFoundError as e:
			self.logger.exception(e, f"Failed to add keywords to {image_path}: {e}")
			raise
		except Exception as e:
			self.logger.exception(e, f"Failed to add keywords to {image_path}: {e}")
			raise

	async def generate_keyword_list_directory(
		self,
		directory_path: str,
		extension_list: List[str],
		save_on_file: bool = False,
		save_on_db: bool = True,
	) -> bool:
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
		engine_path: str = os.path.join(directory_path, KEYWORD_LIST_DB_FILE_NAME)
		engine_conn_str: str = f"sqlite+aiosqlite:////{engine_path}"
		db_engine: AsyncEngine = await init_engine(engine_conn_str)
		session = get_db_session(db_engine)
		async with session() as db:
			for idx, file_name in enumerate(file_name_list):
				ext = os.path.splitext(file_name)[-1].lower()
				file_path = file_name  # os.path.join(subdir, file_name)
				photo_crud = DBCRUD(Photo)
				retrieved_photo = await photo_crud.get_by(db, path=file_path)
				if retrieved_photo is None:
					keyword_list = await self.generate_keyword_list_image(image_path=file_path)
					self.logger.info(f"{os.path.split(file_path)[1]}: {keyword_list}")
					if save_on_db:
						await self.save_to_db(
							db=db, image_path=file_path, keyword_list=keyword_list
						)
					if save_on_file:
						await self.save_to_file(file_path=file_path, keyword_list=keyword_list)
				self.logger.info(f"{idx + 1}/{len(file_name_list)} end")
		return True
