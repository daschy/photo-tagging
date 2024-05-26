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
from models.AIGen import AIGen
from PIL import Image


class AIGenPretrained(AIGen):
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

	async def generate_text(self, img_path: str, prompt: str) -> str:
		with Image.open(img_path) as image:
			loop = asyncio.get_running_loop()
			with ThreadPoolExecutor() as pool:
				if prompt is not None and len(prompt) > 0:
					processor: PaliGemmaProcessor = self.processor
					model_inputs = processor(images=image, text=prompt, return_tensors="pt").to(
						self.device
					)
					input_len = model_inputs["input_ids"].shape[-1]
					generation = await loop.run_in_executor(
						pool,
						lambda: self.model.generate(
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
