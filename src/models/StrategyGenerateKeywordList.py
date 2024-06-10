import asyncio
import os
from glob import glob
from typing import List
import itertools
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from models.AIGen import AIGen
from models.AIGenPaliGemma import AIGenParamsPaliGemma
from models.orm.Photo import Photo
from models.AIGenBert import TOKEN_TYPE, AIGenParamsBert
from models.ExifFileCRUD import ExifFileCRUD
from models.DBCRUD import DBCRUD

from models.ReverseGeotagging import ReverseGeotagging
from models.StrategyBase import StrategyBase
from utils.db_utils_async import get_db_session, init_engine


class StrategyGenerateKeywordList(StrategyBase):
	def __init__(
		self,
		image_to_text_ai_list: List[AIGen[AIGenParamsPaliGemma]],
		token_classification_ai: AIGen[AIGenParamsBert],
		reverse_geotagging: ReverseGeotagging,
	):
		super().__init__()
		self.image_to_text_ai_list: List[AIGen[AIGenParamsPaliGemma]] = (
			image_to_text_ai_list
		)
		self.token_classification_ai: AIGen[AIGenParamsBert] = token_classification_ai
		self.token_classification_ai.ai_init()
		self.reverse_geotagging: ReverseGeotagging = reverse_geotagging
		self.exif_crud = ExifFileCRUD()
		self.db_crud = DBCRUD(Photo)
		for item in self.image_to_text_ai_list:
			item.ai_init()

	def _check_init(self):
		for genai in self.image_to_text_ai_list:
			if not genai.is_init():
				raise ValueError(f"image_to_text_ai {genai.model_id} is not initialized")
		if self.token_classification_ai.is_init() is False:
			raise ValueError("token_classification_ai is not initialized")

	def get_db_name(self) -> str:
		genai_name_list: str = "__".join(
			list(
				dict.fromkeys(
					map(
						lambda item: item.model_id.split("/")[1],
						(self.image_to_text_ai_list + [self.token_classification_ai]),
					)
				)
			)
		)
		return f"keywords__{genai_name_list}.db"

	async def generate_keyword_list_image(self, image_path: str) -> List[str]:
		try:
			self._check_init()
			caption_color_list: List[str] = list(
				await asyncio.gather(
					*[
						genai.generate(file_path=image_path) for genai in self.image_to_text_ai_list
					]
				)
			)  # type: ignore
			text = " ".join(caption_color_list)
			token_list: List[List[str]] = list(
				await asyncio.gather(
					self.token_classification_ai.generate(  # type: ignore
						text=text, token_type=TOKEN_TYPE.NOUN
					),
					self.reverse_geotagging.generate_reverse_geotag(file_path=image_path),
					self.token_classification_ai.generate(  # type: ignore
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
		output = await self.exif_crud.save_keyword_list(
			file_path=file_path, keyword_list=keyword_list
		)
		return output

	async def save_to_db(
		self, db: AsyncSession, image_path: str, keyword_list: List[str]
	) -> bool:
		try:
			new_photo = Photo(image_path)
			new_photo.set_keyword_list(keyword_list)
			await self.db_crud.create(db, new_photo)
			return True
		except FileNotFoundError as e:
			self.logger.exception(e, f"File {image_path}")
			raise
		except Exception as e:
			self.logger.exception(e, "Failed save keywords to db")
			raise

	async def generate_keyword_list_directory(
		self,
		directory_path: str,
		extension_list: List[str],
		exclude_path_list: List[str] = None,  # type: ignore
		save_on_file: bool = False,
	) -> bool:
		file_name_list = self.get_file_list(
			directory_path, extension_list, exclude_path_list
		)
		engine_path: str = os.path.join(directory_path, self.get_db_name())
		engine_conn_str: str = f"sqlite+aiosqlite:////{engine_path}"
		self.logger.info(f"saving keywords to {engine_conn_str}")
		db_engine: AsyncEngine = await init_engine(engine_conn_str)
		session = get_db_session(db_engine)
		async with session() as db:
			for idx, file_path in enumerate(file_name_list):
				file_name = os.path.split(file_path)[1]
				retrieved_photo = await self.db_crud.get_by(db, path=file_path)
				if retrieved_photo is None:
					keyword_list: List[str] = await self.generate_keyword_list_image(
						image_path=file_path
					)
					self.logger.info(f"{file_name}: {keyword_list}")
					await self.save_to_db(db=db, image_path=file_path, keyword_list=keyword_list)
					if save_on_file:
						await self.save_to_file(file_path=file_path, keyword_list=keyword_list)
				else:
					if save_on_file:
						keyword_list: List[str] = retrieved_photo.keyword_list  # type: ignore
						await self.save_to_file(file_path=file_path, keyword_list=keyword_list)
				self.logger.info(f"{file_name}: {idx + 1}/{len(file_name_list)} end")
		return True
