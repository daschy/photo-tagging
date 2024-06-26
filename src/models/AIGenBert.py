from typing import List
import asyncio
from enum import Enum
from typing_extensions import Required
from concurrent.futures import ThreadPoolExecutor
from transformers import (
	pipeline,
	Pipeline,
)
from models.AIGen import AIGen, AIGenParams


class TOKEN_TYPE(Enum):
	NOUN = "NOUN"
	ADJ = "ADJ"


class AIGenParamsBert(AIGenParams):
	token_type: TOKEN_TYPE
	text: Required[str]


class AIGenBert(AIGen[AIGenParamsBert]):
	def __init__(self, model_id: str, aggregation_strategy: str = "simple"):
		super().__init__(model_id=model_id)
		self.aggregation_strategy = aggregation_strategy

	def is_init(
		self,
	) -> bool:
		return self.pipeline and self.model and self.processor

	def ai_init(
		self,
	) -> "AIGen[AIGenParamsBert]":
		self.logger.debug("start create pipeline")
		self.pipeline: Pipeline = pipeline(
			model=self.model_id,
			aggregation_strategy=self.aggregation_strategy,
		)
		self.logger.debug("end create pipeline")
		self.model = self.pipeline.model
		self.processor = self.pipeline.tokenizer
		return self  # type: ignore

	async def generate(
		self,
		**kwargs: AIGenParamsBert,
	) -> List[str]:
		return await self._generate_token_list(
			text=kwargs.get("text"),  # type: ignore
			token_type=kwargs.get(
				"token_type",
			),  # type: ignore
		)

	async def _generate_token_list(self, text: str, token_type: TOKEN_TYPE) -> List[str]:
		if text is None or len(text) == 0:
			raise ValueError("text is null or empty")
		if token_type is None:
			raise ValueError("token type is null")
		loop = asyncio.get_running_loop()
		pip: Pipeline = self.pipeline
		self.logger.debug(f"start tokenization {token_type.value}")
		with ThreadPoolExecutor() as pool:
			tokens: list[dict[str, str]] = await loop.run_in_executor(
				pool,
				lambda: pip.predict(text),  # type: ignore
			)
			output = [
				token["word"] for token in tokens if token["entity_group"] == (token_type.value)
			]
		self.logger.debug(f"end tokenization {token_type.value}")
		return output
