import os
import asyncio
import itertools
from models.AIGen import AIGen
from models.AIGenBert import TOKEN_TYPE, AIGenBert
from models.DBCRUD import DBCRUD
from models.orm.Image import Image
from services.StrategyBaseV2 import StrategyBaseV2
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine


class StrategyGenerateImageDescription(StrategyBaseV2):
	def __init__(
		self,
		ai_gen_list_for_description: list[AIGen],
		ai_gen_tokenization: AIGenBert,
		db_connection_string: str,
	):
		super().__init__()
		self.ai_gen_list_for_description = ai_gen_list_for_description
		self.ai_gen_tokenization = ai_gen_tokenization
		self.db_connection_string = db_connection_string

	async def process_file(
		self, image_path: str, db_session: AsyncSession | None
	) -> list[str]:
		if not os.path.exists(image_path):
			raise FileNotFoundError(image_path)
		caption_and_color_text: list[str] = list(
			await asyncio.gather(
				*[
					genai.generate(file_path=image_path)
					for genai in self.ai_gen_list_for_description
				]
			)
		)  # type: ignore
		text = " ".join(caption_and_color_text)
		token_list: list[list[str]] = list(
			await asyncio.gather(
				self.ai_gen_tokenization.generate(
					text=text,  # type: ignore
					token_type=TOKEN_TYPE.NOUN,  # type: ignore
				),
				self.ai_gen_tokenization.generate(
					text=text,  # type: ignore
					token_type=TOKEN_TYPE.ADJ,  # type: ignore
				),
			)
		)
		output_keyword_list: list[str] = sorted(
			list(set(itertools.chain.from_iterable(token_list))), key=str.casefold
		)

		if db_session:
			db_entry = Image(file_path=image_path).set_keyword_list_description(
				output_keyword_list
			)
			await DBCRUD[Image](Image).create(db_session, db_entry)

		return output_keyword_list

	async def process_directory(
		self,
		directory_path: str,
		extension_list: list[str],
		exclude_path_list: list[str],
		save_on_file: bool,
	) -> bool:
		raise NotImplementedError
