from Utils.LoggerUtils import GetLogger
# import coloredlogs
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List
from transformers import (
    AutoProcessor,
    AutoTokenizer,
    AutoImageProcessor,
    AutoModelForCausalLM,
    BlipForConditionalGeneration,
    VisionEncoderDecoderModel,
)
from transformers import (
    pipeline,
)

from PIL import Image

from Models.Caption import Caption
from Models.AI import AI


git_base = AI(
    processor=AutoProcessor.from_pretrained("microsoft/git-base-coco"),
    model=AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco"),
)

git_large = AI(
    processor=AutoProcessor.from_pretrained("microsoft/git-large-coco"),
    model=AutoModelForCausalLM.from_pretrained("microsoft/git-large-coco"),
)

blip_base = AI(
    processor=AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base"),
    model=BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    ),
)

blip_large = AI(
    processor=AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-large"),
    model=BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-large"
    ),
)

vitgpt = AI(
    processor=AutoImageProcessor.from_pretrained(
        "nlpconnect/vit-gpt2-image-captioning"
    ),
    model=VisionEncoderDecoderModel.from_pretrained(
        "nlpconnect/vit-gpt2-image-captioning"
    ),
    tokenizer=AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning"),
)


async def _generate_caption(ai: AI, image) -> Caption:
    inputs = ai.processor(images=image, return_tensors="pt").to(ai.device)
    executor = ThreadPoolExecutor()
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


async def _generateCaptionList(image) -> List[str]:
    return [
        await _captionToTags(await _generate_caption(git_base, image)),
        await _captionToTags(await _generate_caption(git_large, image)),
        await _captionToTags(await _generate_caption(blip_base, image)),
        await _captionToTags(await _generate_caption(blip_large, image)),
        await _captionToTags(await _generate_caption(vitgpt, image)),
    ]


# Token Classifier
token_classifier = pipeline(
    model="vblagoje/bert-english-uncased-finetuned-pos",
    aggregation_strategy="simple",
)


async def _captionToTags(caption: Caption):
    executor = ThreadPoolExecutor()
    tokens = await asyncio.get_event_loop().run_in_executor(
        executor,
        lambda: token_classifier(caption.text),
    )
    nouns = [token["word"] for token in tokens if token["entity_group"] == "NOUN"]
    return nouns


async def generateCaptionTags(img_path) -> List[str]:
    outputTags: List[str] = []
    with Image.open(img_path) as image:
        captionTagsList = await _generateCaptionList(image)
        for tags in captionTagsList:
            outputTags += tags
    return list(set(outputTags))


async def main():
    img_path = "/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_1759.NEF"
    captions = await generateCaptionTags(img_path)
    log.debug(f"{captions}")


if __name__ == "__main__":
    log = GetLogger(__name__)
    asyncio.run(main())
