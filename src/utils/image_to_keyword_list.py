import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List
from transformers import (
  AutoProcessor,
  PaliGemmaForConditionalGeneration,
  pipeline,
)

from PIL import Image
from src.utils.logger_utils import get_logger
from src.utils import text_token_classification_bert
from src.models.Token import Token
from src.models.AI import AI
from src.models.Caption import Caption


log = get_logger(__name__)

log.debug("Start init AI")
paligemma = AI(
  model=PaliGemmaForConditionalGeneration.from_pretrained(
    "google/paligemma-3b-mix-448"
  ),
  processor=AutoProcessor.from_pretrained("google/paligemma-3b-mix-448"),
)

# Token Classifier
token_classifier = pipeline(
  model="vblagoje/bert-english-uncased-finetuned-pos",
  aggregation_strategy="simple",
)


log.debug("End Init AI")


async def _generate_caption(ai: AI, image: Image, prompt: str) -> Caption:
  loop = asyncio.get_running_loop()
  with ThreadPoolExecutor() as pool:
    if prompt is not None:
      inputs = ai.processor(images=image, text=prompt, return_tensors="pt").to(
        ai.device
      )
      generated_ids = await loop.run_in_executor(
        pool,
        lambda: ai.model.generate(
          **inputs,
          max_new_tokens=50,
          do_sample=False,
        ),
      )
      decoded: str = ai.processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
        padding=False,
      )[0]
      generated_caption: str = decoded.split("\n")[1]
    else:
      inputs = ai.processor(images=image, return_tensors="pt").to(ai.device)
      generated_ids = await loop.run_in_executor(
        pool,
        lambda: ai.model.generate(pixel_values=inputs.pixel_values, max_length=100),
      )
      if ai.tokenizer is not None:
        generated_caption = ai.tokenizer.batch_decode(
          generated_ids, skip_special_tokens=True
        )[0]
      else:
        generated_caption = ai.processor.batch_decode(
          generated_ids, skip_special_tokens=True
        )[0]

  result = Caption(generated_caption, ai.model.name_or_path)
  return result


async def _generate_keyword_list(image: Image) -> List[str]:
  log.debug("Start generate caption list " + (image.filename).split("/")[-1])
  caption_list = await asyncio.gather(
    _generate_caption(paligemma, image, "caption"),
    _generate_caption(paligemma, image, "main 2 colors"),
  )
  log.debug("End generate caption list " + (image.filename).split("/")[-1])
  log.debug("Start tokenize caption list " + (image.filename).split("/")[-1])
  tokenList: List[Token] = await asyncio.gather(
    text_token_classification_bert.TextToTokenList(
      caption_list[0].text, text_token_classification_bert.LABELS.NOUN
    ),
    text_token_classification_bert.TextToTokenList(
      caption_list[1].text, text_token_classification_bert.LABELS.ADJ
    ),
  )
  log.debug("End tokenize caption list " + (image.filename).split("/")[-1])
  output = list(
    set(
      []
      + [token.text for token in tokenList[0]]
      + [token.text for token in tokenList[1]]
    )
  )
  return output


async def generate_keyword_list(img_path: str) -> List[str]:
  output_keyword_list: List[str] = []
  with Image.open(img_path) as image:
    output_keyword_list = await _generate_keyword_list(image)

  output = output_keyword_list
  log.debug(img_path.split("/")[-1] + f": {output}")
  return output


async def main():
  img_path = "/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_1759.NEF"
  captions = await generate_keyword_list(img_path)
  log.info(f"{captions}")


if __name__ == "__main__":
  asyncio.run(main())
