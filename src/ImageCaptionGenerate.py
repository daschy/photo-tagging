from transformers import (
    AutoProcessor,
    AutoTokenizer,
    AutoImageProcessor,
    AutoModelForCausalLM,
    BlipForConditionalGeneration,
    VisionEncoderDecoderModel,
)
from typing import List
import torch
from PIL import Image
from prettyprinter import cpprint as pp
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging

from models.Caption import Caption
from models.AI import AI

device = "cuda" if torch.cuda.is_available() else "cpu"


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
    inputs = ai.processor(images=image, return_tensors="pt").to(device)
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
    log.debug(f"{result}")
    return result


async def generateCaptionList(img_path) -> List[Caption]:
    with Image.open(img_path) as image:
        return [
            await _generate_caption(git_base, image),
            await _generate_caption(git_large, image),
            await _generate_caption(blip_base, image),
            await _generate_caption(blip_large, image),
            await _generate_caption(vitgpt, image),
        ]


async def main():
    img_path = "/Users/1q82/Pictures/Photos/Amsterdam/People/ZDS_1759.NEF"
    captions = await generateCaptionList(img_path)
    for caption in captions:
        log.debug(f"{caption}")


if __name__ == "__main__":
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    logging.basicConfig(
        format="%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s",
        # level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    asyncio.run(main())
