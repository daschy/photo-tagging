import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List
from transformers import (
    AutoProcessor,
    PaliGemmaForConditionalGeneration,
    pipeline,
)

from PIL import Image
from src.Logger.LoggerUtils import GetLogger
from src.Models.Token import Token
from src.Models.AI import AI
from src.Models.Caption import Caption
from src.Utils import TextTokenClassificationBert


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
                lambda: ai.model.generate(
                    pixel_values=inputs.pixel_values, max_length=100
                ),
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


async def _generateKeywordList(image: Image) -> List[str]:
    log.debug("Start generate caption list " + (image.filename).split("/")[-1])
    captionList = await asyncio.gather(
        _generate_caption(paligemma, image, "caption"),
        _generate_caption(paligemma, image, "main 2 colors"),
    )
    log.debug("End generate caption list " + (image.filename).split("/")[-1])
    log.debug("Start tokenize caption list " + (image.filename).split("/")[-1])
    tokenList: List[Token] = await asyncio.gather(
        TextTokenClassificationBert.text_to_tokenList(captionList[0].text, TextTokenClassificationBert.LABELS.NOUN),
        TextTokenClassificationBert.text_to_tokenList(captionList[1].text, TextTokenClassificationBert.LABELS.ADJ),
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


async def generateCaptionTags(img_path: str) -> List[str]:
    outputKeywords: List[str] = []
    with Image.open(img_path) as image:
        outputKeywords = await _generateKeywordList(image)

    output = outputKeywords
    log.debug(img_path.split("/")[-1] + f": {output}")
    return output


async def main():
    img_path = "/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_1759.NEF"
    captions = await generateCaptionTags(img_path)
    log.info(f"{captions}")


if __name__ == "__main__":
    asyncio.run(main())
