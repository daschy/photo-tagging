import os
from typing import Tuple
import asyncio
from concurrent.futures import ThreadPoolExecutor
from transformers import (
	PaliGemmaForConditionalGeneration,
	PaliGemmaProcessor,
	PreTrainedModel,
	ProcessorMixin,
)
from models.AIGen import AIGen, AIGenParams
from PIL import Image


class AIGenParamsPaliGemma(AIGenParams):
	img_path: str


class AIGenPretrained(AIGen[AIGenParamsPaliGemma]):
	def __init__(self, model_id: str):
		super().__init__(model_id=model_id)

	def is_init(
		self,
	) -> bool:
		return self.model is not None and self.processor is not None

	def ai_init(
		self,
	) -> None:
		self.logger.debug("start create model")
		self.model = PaliGemmaForConditionalGeneration.from_pretrained(
			self.model_id, token=os.environ.get("HF_TOKEN")
		)
		self.logger.debug("end create model")
		self.logger.debug("start create processor")
		self.processor = PaliGemmaProcessor.from_pretrained(self.model_id)
		self.logger.debug("end create model")

	async def generate(
		self,
		**kwargs: AIGenParamsPaliGemma,
	) -> str:
		return await self._generate_text(
			file_path=kwargs.get("file_path"),  # type: ignore
			text=kwargs.get("text"),  # type: ignore
		)

	async def _generate_text(self, file_path: str, text: str) -> str:
		with Image.open(file_path) as image:
			loop = asyncio.get_running_loop()
			with ThreadPoolExecutor() as pool:
				if text is not None and len(text) > 0:
					processor: PaliGemmaProcessor = self.processor # type: ignore
					model_inputs = processor(images=image, text=text, return_tensors="pt").to(
						self.device
					)
					input_len = model_inputs["input_ids"].shape[-1]
					generation = await loop.run_in_executor(
						pool,
						lambda: self.model.generate( # type: ignore
							**model_inputs,
							max_new_tokens=50,
							do_sample=False,
						),
					)
					generation = generation[0][input_len:]

					generated_caption: str = processor.decode(
						generation,
						clean_up_tokenization_spaces=False,
						skip_special_tokens=True,
						padding=False,
					)
					return generated_caption
				else:
					raise ValueError("prompt must be not empty")
