from typing import Tuple, List, Enum
import asyncio
from concurrent.futures import ThreadPoolExecutor
from transformers import pipeline, Pipeline, PreTrainedModel, AutoTokenizer
from src.models.AIGen import AIGen


class TOKEN_TYPE(Enum):
  NOUN = "NOUN"
  ADJ = "ADJ"


class AIGenTokenClassification(AIGen):
  def __init__(self, model_id: str):
    super().__init__(model_id=model_id)

  def ai_init(
    self,
  ) -> Tuple[
    PreTrainedModel,
    AutoTokenizer,
  ]:
    self.logger.debug("start create pipeline")
    self.pipeline: Pipeline = pipeline(
      model=self.model_id,
      aggregation_strategy="simple",
    )
    self.logger.debug("end create pipeline")
    self.model = self.pipeline.model
    self.processor = self.pipeline.tokenizer
    return self.model, self.processor

  async def generate_token_list(self, text: str, token_type: TOKEN_TYPE) -> List[str]:
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
