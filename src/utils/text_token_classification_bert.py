import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List
from transformers import (
  pipeline,
)
from enum import Enum
from src.Logger.logger_utils import get_logger
from src.Models_.Token import Token

log = get_logger(__name__)
log.debug("Start init AI")


# Token Classifier
token_classifier = pipeline(
  model="vblagoje/bert-english-uncased-finetuned-pos",
  aggregation_strategy="simple",
)

log.debug("End init AI")


class LABELS(Enum):
  NOUN = "NOUN"
  ADJ = "ADJ"


async def TextToTokenList(text: str, label: LABELS) -> List[Token]:
  loop = asyncio.get_running_loop()
  log.debug("Start tokenization %s", {label.value})
  with ThreadPoolExecutor() as pool:
    tokens = await loop.run_in_executor(
      pool,
      lambda: token_classifier(text),
    )
    output = [
      Token(text=token["word"], score=token["score"], label=token["entity_group"])
      for token in tokens
      if token["entity_group"] == (label.value)
    ]
  log.debug("End tokenization %s", label.value)
  return output


async def main():
  text = "black white A man sits on a blanket in a park, basking in the clear blue sky. The park is filled with people, some lounging on blankets, others riding bikes. The man has long hair and is wearing sunglasses and a black jacket. A red"
  tokens_all = await asyncio.gather(
    TextToTokenList(text, LABELS.ADJ), TextToTokenList(text, LABELS.NOUN)
  )
  log.debug(f"{[token.text for token in tokens_all[0]]}")
  log.debug(f"({[token.text for token in tokens_all[1]]})")


if __name__ == "__main__":
  asyncio.run(main())
