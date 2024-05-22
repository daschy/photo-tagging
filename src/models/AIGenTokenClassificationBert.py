from typing import Tuple, List
import asyncio
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
from transformers import pipeline, Pipeline, PreTrainedModel, AutoTokenizer
from src.models.AIGen import AIGen


class TOKEN_TYPE(Enum):
  NOUN = "NOUN"
  ADJ = "ADJ"


class AIGenTokenClassificationBert(AIGen):
  def __init__(self, model_id: str, aggregation_strategy: str = "simple"):
    super().__init__(model_id=model_id)
    self.aggregation_strategy = aggregation_strategy

  def ai_init(
    self,
  ) -> Tuple[
    PreTrainedModel,
    AutoTokenizer,
  ]:
    self.logger.debug("start create pipeline")
    self.pipeline: Pipeline = pipeline(
      model=self.model_id,
      aggregation_strategy=self.aggregation_strategy,
    )
    self.logger.debug("end create pipeline")
    self.model = self.pipeline.model
    self.processor = self.pipeline.tokenizer
    return self.model, self.processor

  async def generate_token_list(self, text: str, token_type: TOKEN_TYPE) -> List[str]:
    if text is None or len(text) == 0:
      raise ValueError("text is null or empty")
    if token_type is None:
      raise ValueError("token type is null")
    loop = asyncio.get_running_loop()
    pip: Pipeline = self.pipeline
    self.logger.debug(f"start tokenization {token_type.value}")
    with ThreadPoolExecutor() as pool:
      tokens = await loop.run_in_executor(
        pool,
        lambda: pip(text),
      )
      output = [
        token["word"] for token in tokens if token["entity_group"] == (token_type.value)
      ]
    self.logger.debug("end tokenization {token_type.value}")
    return output