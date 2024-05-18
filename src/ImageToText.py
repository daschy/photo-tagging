from Utils.LoggerUtils import GetLogger
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List
from transformers import (
    AutoProcessor,
    PaliGemmaForConditionalGeneration,
    pipeline,
)

from PIL import Image

from Models.Caption import Caption
from Models.AI import AI
from Utils.TextTokenClassificationBert import textToTokens, LABELS
from Utils.Token import Token


log = GetLogger(__name__)

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


async def _generate_caption(ai: AI, image, prompt: str) -> Caption:
    executor = ThreadPoolExecutor()
    if prompt is not None:
        log.debug(f"Start process {ai.model.name_or_path}")
        inputs = ai.processor(images=image, text=prompt, return_tensors="pt").to(
            ai.device
        )
        log.debug(f"End process {ai.model.name_or_path}")
        log.debug(f"Start generate {ai.model.name_or_path}")
        generated_ids = await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: ai.model.generate(
                **inputs,
                max_new_tokens=50,
                do_sample=False,
            ),
        )
        log.debug(f"End generate {ai.model.name_or_path}")
        log.debug(f"Start decode {ai.model.name_or_path}")
        decoded: str = ai.processor.batch_decode(
            generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
            padding=False,
        )[0]
        generated_caption: str = decoded.split("\n")[1]
        log.debug(f"End decode {ai.model.name_or_path}")
    else:
        inputs = ai.processor(images=image, return_tensors="pt").to(ai.device)
        generated_ids = await asyncio.get_event_loop().run_in_executor(
            executor,
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
    log.debug(f"Caption({result.modelName}): {result.text}")
    return result


async def _generateKeywordList(image) -> List[str]:
    captionList = await asyncio.gather(
        _generate_caption(paligemma, image, "caption"),
        _generate_caption(paligemma, image, "main 2 colors"),
    )

    tokenList: List[Token] = await asyncio.gather(
        textToTokens(captionList[0].text, LABELS.NOUN),
        textToTokens(captionList[1].text, LABELS.ADJ),
    )
    output = list(
        set(
            []
            + [token.text for token in tokenList[0]]
            + [token.text for token in tokenList[1]]
        )
    )
    return output


async def _captionToTags(caption: Caption, type: str = None or "NOUN" or "ADJ"):
    executor = ThreadPoolExecutor()
    tokens = await asyncio.get_event_loop().run_in_executor(
        executor,
        lambda: token_classifier(caption.text),
    )
    nouns = [
        token["word"] for token in tokens if token["entity_group"] == (type or "NOUN")
    ]
    return nouns


async def generateCaptionTags(img_path: str) -> List[str]:
    outputKeywords: List[str] = []
    with Image.open(img_path) as image:
        outputKeywords = await _generateKeywordList(image)

    output = outputKeywords
    log.debug(f"{img_path}: {output}")
    return output


async def main():
    img_path = "/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_1759.NEF"
    captions = await generateCaptionTags(img_path)
    log.info(f"{captions}")


if __name__ == "__main__":
    asyncio.run(main())
