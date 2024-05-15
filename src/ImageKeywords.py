from transformers import pipeline
from typing import List
import asyncio
from concurrent.futures import ThreadPoolExecutor


token_classifier = pipeline(
    model="vblagoje/bert-english-uncased-finetuned-pos",
    aggregation_strategy="simple",
)


async def _extract_keywords_from_caption_async(caption):
    executor = ThreadPoolExecutor()
    tokens = await asyncio.get_event_loop().run_in_executor(
        executor,
        lambda: token_classifier(caption),
    )
    nouns = [token["word"] for token in tokens if token["entity_group"] == "NOUN"]
    return nouns


async def captionListToKeywords_async(captionList: List[str]) -> List[str]:
    merged_array = []
    for caption in captionList:
        keywords = await _extract_keywords_from_caption_async(caption)
        merged_array.extend(keywords)
    return list(set(merged_array))


async def main():
    image_captions = [
        "a woman sitting on a grassy field with a bunch of people",
        "man in the middle",
    ]
    keywords = await captionListToKeywords_async(image_captions)
    print(keywords)


# Run the asynchronous function
asyncio.run(main())
